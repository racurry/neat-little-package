# Box Factory Development Guidelines

**Knowledge Delta Only:** Components should only contain what Claude would get wrong without them. Fetch official docs and verify against real behavior before deciding something is "obvious." Claude has a strong tendency to assume it knows things rather than checking.

**Skills over Agents:** Custom agents earn their keep through tool restrictions. If tool restrictions don't matter, put the process steps in a skill instead.

**Defer to Official Docs:** Never hardcode model names, tool lists, or syntax. Point to official documentation URLs and let Claude fetch current specs.
