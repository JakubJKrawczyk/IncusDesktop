
class GlobalHelpers:

    class StrHelper:

        @staticmethod
        def parse_table(text: str) -> dict[str, list[str]]:
            """First token = key, rest = values as strings. Any /proc-style file."""

            return {
                (parts := line.split())[0]: parts[1:]
                for line in text.splitlines() if line.strip()
            }