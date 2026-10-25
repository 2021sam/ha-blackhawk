"""Conversation platform for Jarvis."""

from __future__ import annotations

import aiohttp
import re

from homeassistant.helpers.storage import Store

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform, intent


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: entity_platform.AddEntitiesCallback,
) -> None:
    """Set up the Jarvis conversation entity."""
    async_add_entities([JarvisConversationEntity(entry)])


class JarvisConversationEntity(conversation.ConversationEntity):
    """Jarvis conversation agent."""

    _attr_name = "Jarvis"
    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize Jarvis."""
        self._entry = entry
        self._speaker_store = None
        self._speaker_preferences = {}
        self._speaker_pending = set()
        self._response_tone_store = None
        self._response_tone_preferences = {}
        self._attr_unique_id = f"{entry.entry_id}_jarvis"

    async def _load_speaker_preferences(self):
        if self._speaker_store is None:
            self._speaker_store = Store(
                self.hass,
                1,
                "jarvis_speaker_preferences",
            )
            data = await self._speaker_store.async_load()
            self._speaker_preferences = (
                data if isinstance(data, dict) else {}
            )

    async def _handle_response_tone_command(self, device_id, text):
        """Manage response-tone preference for the originating device."""
        await self._load_response_tone_preferences()

        command = re.sub(r"[^a-z0-9 ]", " ", text.lower())
        command = " ".join(command.split())
        command = re.sub(r"^(?:hey )?jarvis\\s+", "", command)

        match = re.fullmatch(
            r"(enable|disable|turn on|turn off) "
            r"(?:the |my )?(?:response|confirmation|wake) tone",
            command,
        )

        if match:
            enabled = match.group(1) in ("enable", "turn on")
            self._response_tone_preferences[device_id] = enabled
            await self._response_tone_store.async_save(
                self._response_tone_preferences
            )
            return "Response tone enabled." if enabled else "Response tone disabled."

        if command in (
            "response tone status",
            "is response tone enabled",
            "is response tone disabled",
            "confirmation tone status",
            "wake tone status",
        ):
            enabled = self._response_tone_preferences.get(device_id, True)
            return "Response tone is enabled." if enabled else "Response tone is disabled."

        return None

    async def _load_response_tone_preferences(self):
        """Load persistent per-device response-tone settings."""
        if self._response_tone_store is None:
            self._response_tone_store = Store(
                self.hass, 1, "jarvis_response_tone_preferences"
            )
            data = await self._response_tone_store.async_load()
            self._response_tone_preferences = (
                data if isinstance(data, dict) else {}
            )

    async def _handle_speaker_command(self, device_id, text):
        # JARVIS_SAFE_SPEAKER_COMMANDS_V2
        await self._load_speaker_preferences()

        speakers = {
            "1": ("local", "This Pixel"),
            "2": ("media_player.amp_1", "Family Room"),
            "3": ("media_player.amp_2", "Upstairs"),
        }

        command = re.sub(r"[^a-z0-9 ]", " ", text.lower())
        command = " ".join(command.split())

        # Remove an optional wake-word prefix.
        command = re.sub(r"^hey jarvis ", "", command)
        command = re.sub(r"^jarvis ", "", command)

        async def select(number):
            self._speaker_preferences[device_id] = number
            await self._speaker_store.async_save(
                self._speaker_preferences
            )
            self._speaker_pending.discard(device_id)
            return f"Using {speakers[number][1]}."

        def identify(value):
            value = value.strip()

            # Remove optional articles and possessives.
            value = re.sub(r"^(the|my|this)\s+", "", value)

            # Remove a trailing device descriptor.
            value = re.sub(
                r"\s+(speaker|amplifier|amp)$",
                "",
                value,
            )

            aliases = {
                "1": (
                    "pixel", "phone", "device", "local",
                    "built in", "built in speaker",
                    "speaker one", "speaker 1",
                    "one", "1",
                ),
                "2": (
                    "family room", "downstairs",
                    "speaker two", "speaker 2",
                    "two", "2",
                ),
                "3": (
                    "upstairs",
                    "speaker three", "speaker 3",
                    "three", "3",
                ),
            }

            for number, names in aliases.items():
                if value in names:
                    return number

            return None

        # Current selection: recognize natural question variations.
        if re.fullmatch(
            r"(what|which) speaker (am i|are you|is jarvis) using",
            command,
        ) or command in (
            "current speaker",
            "what is my current speaker",
            "where are you speaking",
        ):
            number = self._speaker_preferences.get(device_id, "1")
            label = speakers.get(number, speakers["1"])[1]
            return f"Your selected speaker is {label}."

        # JARVIS_SPEAKER_DISCOVERY_V1
        configured_commands = (
            "what speakers are available",
            "which speakers are available",
            "list speakers",
            "list available speakers",
            "show speakers",
            "what are my speakers",
        )

        discovery_commands = (
            "discover speakers",
            "find speakers",
            "scan for speakers",
            "discover media players",
        )

        if command in configured_commands:
            descriptions = ["One, this Pixel, local"]

            for number in ("2", "3"):
                entity_id, label = speakers[number]
                state = self.hass.states.get(entity_id)

                available = (
                    state is not None
                    and state.state not in ("unknown", "unavailable")
                )

                status = "available" if available else "unavailable"
                descriptions.append(
                    f"{number}, {label}, {status}"
                )

            return (
                "Configured speakers: "
                + "; ".join(descriptions)
                + ". Say discover speakers to find other devices."
            )

        if command in discovery_commands:
            configured_ids = {
                "media_player.amp_1",
                "media_player.amp_2",
            }

            discovered = []

            for state in self.hass.states.async_all("media_player"):
                if state.entity_id in configured_ids:
                    continue

                if state.state in ("unknown", "unavailable"):
                    continue

                name = state.attributes.get(
                    "friendly_name",
                    state.entity_id,
                )

                discovered.append(
                    f"{name}, {state.entity_id}"
                )

            if not discovered:
                return (
                    "No additional available media players found. "
                    "Your configured speakers remain unchanged."
                )

            return (
                "Additional available media players: "
                + "; ".join(sorted(discovered))
                + ". These devices have not been added to "
                  "Jarvis speaker selection."
            )

        # Cancel or repeat a pending selection.
        if command in ("cancel", "cancel speaker selection"):
            if device_id in self._speaker_pending:
                self._speaker_pending.discard(device_id)
                return "Speaker selection canceled."
            return None

        if command in ("repeat options", "repeat speakers"):
            if device_id in self._speaker_pending:
                return (
                    "One, this Pixel. Two, Family Room. "
                    "Three, Upstairs. Which speaker?"
                )
            return "Say what speakers are available."

        # Recognize natural direct commands.
        prefixes = (
            r"(?:please )?",
            r"(?:(?:can|could|would) you please )?",
            r"(?:(?:can|could|would) you )?",
        )

        actions = (
            r"(?:change|switch|set) "
            r"(?:(?:my|the) )?"
            r"(?:speaker|audio output|output) to ",
            r"switch to ",
            r"use ",
            r"play (?:audio|responses) (?:on|through) ",
            r"speak (?:on|through) ",
        )

        target = None

        for polite in prefixes:
            for action in actions:
                match = re.fullmatch(
                    polite + action + r"(.+)",
                    command,
                )
                if match:
                    target = match.group(1)
                    break
            if target is not None:
                break

        if target is not None:
            number = identify(target)

            if number:
                return await select(number)

            # Never forward an unrecognized speaker target
            # to the general AI.
            return (
                "I couldn't identify that audio output. "
                "Say Pixel, Family Room, or Upstairs."
            )

        # A request to change speakers without a target.
        if command in (
            "change speaker",
            "switch speaker",
            "select speaker",
            "change my speaker",
            "switch my speaker",
        ):
            self._speaker_pending.add(device_id)
            return (
                "Which speaker? "
                "One, this Pixel; two, Family Room; "
                "three, Upstairs."
            )

        # A pending selection may be answered by name or number.
        if device_id in self._speaker_pending:
            number = identify(command)
            if number:
                return await select(number)

        # Explicit speaker-number commands.
        if command.startswith("speaker "):
            number = identify(command)
            if number:
                return await select(number)

            return (
                "I couldn't identify that speaker. "
                "Say Pixel, Family Room, or Upstairs."
            )

        return None

    # JARVIS_EXTERNAL_TTS_V2
    async def _route_speech(self, device_id, message):
        """Play through selected speaker or return speech for Pixel."""
        await self._load_speaker_preferences()

        selected = self._speaker_preferences.get(device_id, "1")

        players = {
            "2": "media_player.amp_1",
            "3": "media_player.amp_2",
        }

        player = players.get(selected)

        # Option 1, or an unknown preference, uses the Pixel.
        if not player:
            return message

        state = self.hass.states.get(player)

        if state is None or state.state in ("unavailable", "unknown"):
            return (
                f"{message} "
                "The selected external speaker is unavailable. "
                "Using this Pixel instead."
            )

        try:
            await self.hass.services.async_call(
                "media_player",
                "volume_mute",
                {
                    "entity_id": player,
                    "is_volume_muted": False,
                },
                blocking=True,
            )

            await self.hass.services.async_call(
                "tts",
                "speak",
                {
                    "entity_id": "tts.google_translate_en_com",
                    "media_player_entity_id": player,
                    "message": message,
                },
                blocking=True,
            )

            # Return the complete answer to Assist for display.
            # Pixel audio may also play alongside external TTS.
            return message

        except Exception:
            return (
                f"{message} "
                "External speaker playback failed. "
                "Using this Pixel instead."
            )

    @property
    def supported_languages(self) -> list[str]:
        """Return supported languages."""
        return ["en"]

    async def _async_handle_message(
        self,
        user_input: conversation.ConversationInput,
        chat_log: conversation.ChatLog,
    ) -> conversation.ConversationResult:
        """Send recognized text to Jarvis."""

        # JARVIS_SPEAKER_REGISTRY_V1
        device_id = user_input.device_id or "home-assistant"
        speaker_reply = await self._handle_response_tone_command(
            device_id, user_input.text
        )
        if speaker_reply is None:
            speaker_reply = await self._handle_speaker_command(
                device_id, user_input.text
            )

        if speaker_reply is not None:
            response = intent.IntentResponse(language=user_input.language)
            routed_reply = await self._route_speech(
                device_id, speaker_reply
            )
            response.async_set_speech(routed_reply)

            chat_log.async_add_assistant_content_without_tools(
                conversation.AssistantContent(
                    agent_id=user_input.agent_id,
                    content=speaker_reply,
                )
            )

            return conversation.ConversationResult(
                conversation_id=user_input.conversation_id,
                response=response,
                continue_conversation=False,
            )

        url = f"{self._entry.data['url']}/ask"

        payload = {
            "message": user_input.text,
            "device_id": user_input.device_id or "home-assistant",
            "room": None,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    response.raise_for_status()
                    data = await response.json()

            answer = str(data.get("answer", "")).strip()

            if not answer:
                answer = "Jarvis returned an empty response."

        except Exception as err:
            answer = f"Jarvis is unavailable: {err}"

        chat_log.async_add_assistant_content_without_tools(
            conversation.AssistantContent(
                agent_id=user_input.agent_id,
                content=answer,
            )
        )

        response = intent.IntentResponse(
            language=user_input.language,
        )
        routed_answer = await self._route_speech(
            device_id, answer
        )
        response.async_set_speech(routed_answer)

        return conversation.ConversationResult(
            conversation_id=user_input.conversation_id,
            response=response,
            continue_conversation=False,
        )
