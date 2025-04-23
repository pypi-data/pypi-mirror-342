import aksharamukha.transliterate
import enum


class VedicSvaraOption(enum.Enum):
	ENABLED = enum.auto()
	DISABLED = enum.auto()


class Script(enum.Enum):
	DEVANAGARI = enum.auto()
	LATIN_ISO = enum.auto()


def _to_api_script(script: Script) -> str:
	return {
		Script.DEVANAGARI: "Devanagari",
		Script.LATIN_ISO: "ISO",
	}[script]


def _wrapped_api(source: Script, target: Script, text: str) -> str | None:
	source_wrapped = _to_api_script(source)
	target_wrapped = _to_api_script(target)

	result = aksharamukha.transliterate.process(source_wrapped, target_wrapped, text)
	if result is None:
		return None
	else:
		return str(result)


def dev_to_latiniso(nagari: str) -> str | None:
	return _wrapped_api(Script.DEVANAGARI, Script.LATIN_ISO, nagari)
