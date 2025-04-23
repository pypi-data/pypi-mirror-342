from dataclasses import dataclass

import numpy as np
from loguru import logger

from bithuman.audio import resample

try:
    from bithuman_local_voice import BithumanLocalSTT as BithumanSTTImpl
except ImportError:
    raise ImportError(
        "bithuman_local_voice is required, please install it with `pip install bithuman_local_voice`"
    )
try:
    from livekit.agents import utils
    from livekit.agents.stt import (
        STT,
        SpeechData,
        SpeechEvent,
        SpeechEventType,
        STTCapabilities,
    )
    from livekit.agents.types import NOT_GIVEN, APIConnectOptions, NotGivenOr
except ImportError:
    raise ImportError(
        "livekit is required, please install it with `pip install livekit-agents`"
    )


@dataclass
class _STTOptions:
    locale: str = "en-US"
    on_device: bool = True
    punctuation: bool = True
    debug: bool = False


class BithumanLocalSTT(STT):
    _SAMPLE_RATE = 16000

    def __init__(
        self, *, locale="en-US", on_device=True, punctuation=True, debug=False
    ):
        capabilities = STTCapabilities(streaming=False, interim_results=False)
        super().__init__(capabilities=capabilities)
        self._opts = _STTOptions(
            locale=locale, on_device=on_device, punctuation=punctuation, debug=debug
        )
        self._stt_impl = BithumanSTTImpl(
            locale=locale, on_device=on_device, punctuation=punctuation, debug=debug
        )

    async def _recognize_impl(
        self,
        buffer: utils.audio.AudioBuffer,
        *,
        language: NotGivenOr[str] = NOT_GIVEN,
        conn_options: APIConnectOptions,
    ):
        if utils.is_given(language) and language != self._opts.locale:
            try:
                await self._stt_impl.set_locale(language)
                self._opts.locale = language
            except Exception as e:
                logger.error(f"Failed to set locale: {e}")

        frame = utils.audio.combine_frames(buffer)
        audio_data = np.frombuffer(frame.data, dtype=np.int16)
        if frame.sample_rate != self._SAMPLE_RATE:
            audio_data = resample(audio_data, frame.sample_rate, self._SAMPLE_RATE)

        result = await self._stt_impl.recognize(
            audio_data, sample_rate=self._SAMPLE_RATE
        )

        return SpeechEvent(
            type=SpeechEventType.FINAL_TRANSCRIPT,
            request_id="",
            alternatives=[
                SpeechData(
                    language=self._opts.locale,
                    text=result["text"],
                    confidence=result["confidence"],
                )
            ],
        )

    async def aclose(self):
        await self._stt_impl.stop()
