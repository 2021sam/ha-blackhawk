"""Config flow for Jarvis Conversation."""

import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN


class JarvisConversationConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Configure Jarvis Conversation."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle initial setup."""

        if user_input is not None:
            await self.async_set_unique_id("jarvis-home-hub")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Jarvis",
                data={
                    "url": user_input["url"].rstrip("/"),
                },
            )

        schema = vol.Schema(
            {
                vol.Required(
                    "url",
                    default="http://10.0.0.250:8001",
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
