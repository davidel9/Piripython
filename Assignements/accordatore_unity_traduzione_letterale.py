"""
Traduzione letterale in Python degli script Unity/C# forniti.

NOTA IMPORTANTE:
Questo file NON sostituisce Unity e non e' pensato per funzionare come gioco/app reale.
Contiene una traduzione il piu' possibile fedele di classi, campi, metodi e flusso logico.
Le API Unity (MonoBehaviour, GameObject, AudioSource, ScrollRect, Coroutine, ecc.) sono imitate
con classi stub/minimali solo per mantenere la struttura originale.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Generator, List, Optional, Sequence


# ============================================================
# STUB / EMULAZIONE MINIMA DI UNITY
# ============================================================


@dataclass
class Color:
    r: float
    g: float
    b: float
    a: float = 1.0


Color.white = Color(1.0, 1.0, 1.0, 1.0)
Color.green = Color(0.0, 1.0, 0.0, 1.0)
Color.yellow = Color(1.0, 0.9215686275, 0.0156862745, 1.0)


@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: "Vector2") -> "Vector2":
        self.x += other.x
        self.y += other.y
        return self


@dataclass
class Vector3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __mul__(self, scalar: float) -> "Vector3":
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)


Vector3.one = Vector3(1.0, 1.0, 1.0)


@dataclass
class Rect:
    center: Vector2 = field(default_factory=Vector2)


class Mathf:
    PI = math.pi

    @staticmethod
    def Abs(value: float) -> float:
        return abs(value)

    @staticmethod
    def Lerp(a: Any, b: Any, t: float) -> Any:
        if isinstance(a, Vector2) and isinstance(b, Vector2):
            return Vector2(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t)
        if isinstance(a, Vector3) and isinstance(b, Vector3):
            return Vector3(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t, a.z + (b.z - a.z) * t)
        return a + (b - a) * t

    @staticmethod
    def RoundToInt(value: float) -> int:
        return int(round(value))

    @staticmethod
    def Log(value: float, base: float) -> float:
        return math.log(value, base)

    @staticmethod
    def Pow(value: float, power: float) -> float:
        return math.pow(value, power)

    @staticmethod
    def Clamp(value: int, min_value: int, max_value: int) -> int:
        return max(min_value, min(value, max_value))

    @staticmethod
    def Sin(value: float) -> float:
        return math.sin(value)

    @staticmethod
    def Exp(value: float) -> float:
        return math.exp(value)


class Time:
    deltaTime: float = 1.0 / 60.0


class AudioSettings:
    @staticmethod
    def dspTime() -> float:
        return time.time()


class MonoBehaviour:
    def StartCoroutine(self, coroutine: Generator[Any, None, None]) -> None:
        # In Unity la coroutine viene distribuita su piu' frame.
        # Qui viene consumata subito per conservare la chiamata, non il timing reale.
        try:
            for _ in coroutine:
                pass
        except TypeError:
            pass

    def GetComponent(self, component_type: Any) -> Any:
        return None


class WaitForEndOfFrame:
    pass


class WaitForSeconds:
    def __init__(self, seconds: float):
        self.seconds = seconds


class PointerEventData:
    pass


class TextMeshProUGUI:
    def __init__(self, text: str = ""):
        self.text = text
        self.color = Color.white


class GameObject:
    def __init__(self, name: str = ""):
        self.name = name
        self.activeSelf = True
        self.components: dict[Any, Any] = {}
        self.transform = Transform()

    def SetActive(self, active: bool) -> None:
        self.activeSelf = active

    def AddComponent(self, component_type: Any) -> Any:
        component = component_type()
        self.components[component_type] = component
        return component

    def GetComponent(self, component_type: Any) -> Any:
        return self.components.get(component_type)


class Transform:
    def __init__(self):
        self.localScale = Vector3.one


class RectTransform(Transform):
    def __init__(self, name: str = ""):
        super().__init__()
        self.name = name
        self.anchoredPosition = Vector2()
        self.position = Vector3()
        self.rect = Rect(center=Vector2())
        self.children: List[RectTransform] = []
        self.components: dict[Any, Any] = {}

    @property
    def childCount(self) -> int:
        return len(self.children)

    def GetChild(self, i: int) -> "RectTransform":
        return self.children[i]

    def InverseTransformPoint(self, position: Vector3) -> Vector3:
        return position

    def GetComponent(self, component_type: Any) -> Any:
        return self.components.get(component_type)


class Image:
    def __init__(self):
        self.color = Color.white
        self.rectTransform = RectTransform()

    def GetComponent(self, component_type: Any) -> Any:
        if component_type is RectTransform:
            return self.rectTransform
        return None


class ScrollRect:
    def __init__(self):
        self.decelerationRate = 0.0
        self.viewport: Optional[RectTransform] = None
        self.velocity = Vector2()


class LayoutRebuilder:
    @staticmethod
    def ForceRebuildLayoutImmediate(content_panel: RectTransform) -> None:
        pass


class FFTWindow:
    BlackmanHarris = "BlackmanHarris"


class AudioClip:
    def __init__(self, name: str = "", length: int = 0, channels: int = 1, frequency: int = 44100, stream: bool = False):
        self.name = name
        self.length = length
        self.channels = channels
        self.frequency = frequency
        self.stream = stream
        self.data: List[float] = []

    @staticmethod
    def Create(name: str, length: int, channels: int, frequency: int, stream: bool) -> "AudioClip":
        return AudioClip(name, length, channels, frequency, stream)

    def SetData(self, samples: Sequence[float], offset_samples: int) -> None:
        self.data = list(samples)


class AudioSource:
    def __init__(self):
        self.loop = False
        self.volume = 1.0
        self.clip: Optional[AudioClip] = None
        self.isPlaying = False
        self.spectrum_provider: Optional[Callable[[List[float]], None]] = None

    def Play(self) -> None:
        self.isPlaying = True

    def PlayOneShot(self, clip: AudioClip) -> None:
        pass

    def GetSpectrumData(self, spectrum: List[float], channel: int, window: Any) -> None:
        if self.spectrum_provider is not None:
            self.spectrum_provider(spectrum)


class Microphone:
    devices: List[str] = []

    @staticmethod
    def GetDeviceCaps(device_name: Optional[str]) -> tuple[int, int]:
        return (0, 48000)

    @staticmethod
    def Start(device_name: Optional[str], loop: bool, length_sec: int, frequency: int) -> AudioClip:
        return AudioClip("Microphone", frequency * length_sec, 1, frequency, False)

    @staticmethod
    def GetPosition(device_name: Optional[str]) -> int:
        return 1


class Permission:
    Microphone = "android.permission.RECORD_AUDIO"
    microphone_authorized = True

    @staticmethod
    def HasUserAuthorizedPermission(permission: str) -> bool:
        return Permission.microphone_authorized

    @staticmethod
    def RequestUserPermission(permission: str) -> None:
        pass


class SceneManager:
    loaded_scene: Optional[str] = None

    @staticmethod
    def LoadScene(scene_name: str) -> None:
        SceneManager.loaded_scene = scene_name


# ============================================================
# ControlloreRullo.cs
# ============================================================


class ControlloreRullo(MonoBehaviour):
    def __init__(self):
        # [Header("Riferimenti")]
        self.contentPanel: Optional[RectTransform] = None

        # [Header("Impostazioni")]
        self.velocitaSnapping: float = 15.0
        self.sogliaFrenata: float = 50.0

        # [Header("Colori e Scale")]
        self.scalaCentrale: float = 1.0
        self.scalaLaterale: float = 0.5
        self.coloreCentrale: Color = Color(0.17, 0.69, 0.70, 1.0)
        self.coloreLaterale: Color = Color(0.12, 0.36, 0.37, 0.4)

        self.ValoreSelezionato: int = 0

        self.scrollRect: ScrollRect = ScrollRect()
        self.viewportRect: Optional[RectTransform] = None
        self.numeriRects: List[RectTransform] = []
        self.staTrascinando: bool = False

    def Start(self) -> None:
        self.scrollRect.decelerationRate = 0.5
        self.viewportRect = self.scrollRect.viewport if self.scrollRect.viewport is not None else RectTransform()

        if self.contentPanel is not None:
            for i in range(self.contentPanel.childCount):
                self.numeriRects.append(self.contentPanel.GetChild(i))

        self.StartCoroutine(self.InizializzazioneMobile())

    def InizializzazioneMobile(self) -> Generator[Any, None, None]:
        yield WaitForEndOfFrame()
        if self.contentPanel is not None:
            LayoutRebuilder.ForceRebuildLayoutImmediate(self.contentPanel)
        yield WaitForSeconds(0.1)

        if len(self.numeriRects) >= 14:
            self.CentraIndice(2, centraggioIstantaneo=True)

    def Update(self) -> None:
        if len(self.numeriRects) < 14:
            return

        indicePiuVicino = self.TrovaIndicePiuVicinoAlCentro()

        if indicePiuVicino >= 12:
            self.TeletrasportoInvisibile(indicePiuVicino, indicePiuVicino - 10)
            indicePiuVicino -= 10
        elif indicePiuVicino <= 1:
            self.TeletrasportoInvisibile(indicePiuVicino, indicePiuVicino + 10)
            indicePiuVicino += 10

        self.AggiornaEffettiVisivi(indicePiuVicino)
        self.EstraiValore(indicePiuVicino)

        if (not self.staTrascinando) and Mathf.Abs(self.scrollRect.velocity.y) < self.sogliaFrenata:
            self.scrollRect.velocity = Vector2(0.0, 0.0)
            self.CentraIndice(indicePiuVicino, centraggioIstantaneo=False)

    def TeletrasportoInvisibile(self, indiceFinto: int, indiceReale: int) -> None:
        if self.contentPanel is None:
            return
        offsetY = self.numeriRects[indiceFinto].anchoredPosition.y - self.numeriRects[indiceReale].anchoredPosition.y
        self.contentPanel.anchoredPosition += Vector2(0.0, offsetY)
        self.numeriRects[indiceReale].localScale = self.numeriRects[indiceFinto].localScale
        testo_reale = self.numeriRects[indiceReale].GetComponent(TextMeshProUGUI)
        testo_finto = self.numeriRects[indiceFinto].GetComponent(TextMeshProUGUI)
        if testo_reale is not None and testo_finto is not None:
            testo_reale.color = testo_finto.color

    def TrovaIndicePiuVicinoAlCentro(self) -> int:
        indice = 0
        distanzaMinima = float("inf")
        centroLocaleY = self.viewportRect.rect.center.y if self.viewportRect is not None else 0.0

        for i in range(len(self.numeriRects)):
            posLocale = self.viewportRect.InverseTransformPoint(self.numeriRects[i].position) if self.viewportRect is not None else self.numeriRects[i].position
            distanza = Mathf.Abs(posLocale.y - centroLocaleY)
            if distanza < distanzaMinima:
                distanzaMinima = distanza
                indice = i
        return indice

    def CentraIndice(self, indice: int, centraggioIstantaneo: bool) -> None:
        if self.contentPanel is None or self.viewportRect is None:
            return
        posLocaleTarget = self.viewportRect.InverseTransformPoint(self.numeriRects[indice].position)
        offsetY = self.viewportRect.rect.center.y - posLocaleTarget.y
        nuovaPos = Vector2(self.contentPanel.anchoredPosition.x, self.contentPanel.anchoredPosition.y)

        if centraggioIstantaneo or Mathf.Abs(offsetY) < 0.5:
            nuovaPos.y += offsetY
        else:
            nuovaPos.y = Mathf.Lerp(nuovaPos.y, nuovaPos.y + offsetY, Time.deltaTime * self.velocitaSnapping)

        self.contentPanel.anchoredPosition = nuovaPos

    def AggiornaEffettiVisivi(self, indiceCentrale: int) -> None:
        for i in range(len(self.numeriRects)):
            alCentro = i == indiceCentrale
            targetScale = self.scalaCentrale if alCentro else self.scalaLaterale
            self.numeriRects[i].localScale = Mathf.Lerp(
                self.numeriRects[i].localScale,
                Vector3.one * targetScale,
                Time.deltaTime * 15.0,
            )
            testo = self.numeriRects[i].GetComponent(TextMeshProUGUI)
            if testo is not None:
                testo.color = self.coloreCentrale if alCentro else self.coloreLaterale

    def EstraiValore(self, indice: int) -> None:
        try:
            self.ValoreSelezionato = int(self.numeriRects[indice].name)
        except (ValueError, IndexError):
            pass

    def OnPointerDown(self, eventData: PointerEventData) -> None:
        self.staTrascinando = True

    def OnDrag(self, eventData: PointerEventData) -> None:
        self.staTrascinando = True

    def OnPointerUp(self, eventData: PointerEventData) -> None:
        self.staTrascinando = False


# ============================================================
# GestoreTotaleBpm.cs
# ============================================================


class GestoreTotaleBpm(MonoBehaviour):
    def __init__(self):
        self.metronomo: Optional[MetronomeControllore] = None
        self.rulloCentinaia: Optional[ControlloreRullo] = None
        self.rulloDecine: Optional[ControlloreRullo] = None
        self.rulloUnita: Optional[ControlloreRullo] = None
        self.bpmAttuale: int = -1

    def Update(self) -> None:
        if self.rulloCentinaia is None or self.rulloDecine is None or self.rulloUnita is None:
            return

        nuovoBpm = (
            self.rulloCentinaia.ValoreSelezionato * 100
            + self.rulloDecine.ValoreSelezionato * 10
            + self.rulloUnita.ValoreSelezionato
        )

        if nuovoBpm < 1:
            nuovoBpm = 1

        if nuovoBpm != self.bpmAttuale:
            self.bpmAttuale = nuovoBpm
            if self.metronomo is not None:
                self.metronomo.ImpostaBPM(self.bpmAttuale)


# ============================================================
# GuitarTuner.cs
# ============================================================


class GuitarTuner(MonoBehaviour):
    def __init__(self):
        self.noteText: Optional[TextMeshProUGUI] = None
        self.feedbackText: Optional[TextMeshProUGUI] = None
        self.iconaIisa: Optional[GameObject] = None
        self.iconaCala: Optional[GameObject] = None
        self.iconaPerfetto: Optional[GameObject] = None

        self.audioSource: Optional[AudioSource] = None
        self.notes: List[str] = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.spectrum: List[float] = [0.0] * 8192
        self.sampleRate: int = 0
        self.isMicInitialized: bool = False
        self.orangeCustom: Color = Color(255.0 / 255.0, 73.0 / 255.0, 4.0 / 255.0)

    def Start(self) -> None:
        self.audioSource = AudioSource()
        self.audioSource.loop = True
        self.audioSource.volume = 1.0

        if self.noteText is not None:
            self.noteText.color = Color.white

        self.NascondiTutteLeIcone()

        if not Permission.HasUserAuthorizedPermission(Permission.Microphone):
            Permission.RequestUserPermission(Permission.Microphone)

    def Update(self) -> None:
        if (not self.isMicInitialized) and Permission.HasUserAuthorizedPermission(Permission.Microphone):
            self.TryStartMicrophone()

        if self.isMicInitialized and self.audioSource is not None and self.audioSource.isPlaying:
            self.AnalyzeSound()

    def TryStartMicrophone(self) -> None:
        if len(Microphone.devices) > 0:
            minFreq, maxFreq = Microphone.GetDeviceCaps(None)
            self.sampleRate = maxFreq if maxFreq != 0 else 48000
            if self.audioSource is not None:
                self.audioSource.clip = Microphone.Start(None, True, 10, self.sampleRate)
                while not (Microphone.GetPosition(None) > 0):
                    pass
                self.audioSource.Play()
            self.isMicInitialized = True

    def AnalyzeSound(self) -> None:
        if self.audioSource is None:
            return
        self.audioSource.GetSpectrumData(self.spectrum, 0, FFTWindow.BlackmanHarris)
        maxV = 0.0
        maxN = 0

        for i in range(len(self.spectrum)):
            if self.spectrum[i] > maxV and self.spectrum[i] > 0.001:
                maxV = self.spectrum[i]
                maxN = i

        trueFundamentalN = maxN
        divisors = [4, 3, 2]
        for d in divisors:
            subN = maxN // d
            if subN > 0 and subN < len(self.spectrum):
                if self.spectrum[subN] > (maxV * 0.15) and self.spectrum[subN] > 0.001:
                    trueFundamentalN = subN

        freqN = float(trueFundamentalN)
        if trueFundamentalN > 0 and trueFundamentalN < len(self.spectrum) - 1:
            dL = self.spectrum[trueFundamentalN - 1] / self.spectrum[trueFundamentalN]
            dR = self.spectrum[trueFundamentalN + 1] / self.spectrum[trueFundamentalN]
            freqN += 0.5 * (dR * dR - dL * dL)

        pitchValue = freqN * (float(self.sampleRate) / 2.0) / len(self.spectrum)

        if pitchValue > 60.0 and pitchValue < 1200.0:
            self.UpdateUI(pitchValue)

    def UpdateUI(self, frequency: float) -> None:
        noteIndex = Mathf.RoundToInt(12.0 * Mathf.Log(frequency / 440.0, 2.0) + 69.0)
        if noteIndex < 0:
            return

        noteName = self.notes[noteIndex % 12]
        targetFreq = 440.0 * Mathf.Pow(2.0, (noteIndex - 69.0) / 12.0)
        diff = frequency - targetFreq

        if self.noteText is not None:
            self.noteText.text = noteName

        self.NascondiTutteLeIcone()

        if Mathf.Abs(diff) < 1.0:
            if self.noteText is not None:
                self.noteText.color = Color.green
            if self.iconaPerfetto is not None:
                self.iconaPerfetto.SetActive(True)
            if self.feedbackText is not None:
                self.feedbackText.text = "APPO'! \n(" + format(frequency, ".1f") + " Hz)"
                self.feedbackText.color = Color.green
        elif diff > 0:
            if self.noteText is not None:
                self.noteText.color = self.orangeCustom
            if self.iconaCala is not None:
                self.iconaCala.SetActive(True)
            if self.feedbackText is not None:
                self.feedbackText.text = "cala anticchia \n(" + format(frequency, ".1f") + " Hz)"
                self.feedbackText.color = self.orangeCustom
        else:
            if self.noteText is not None:
                self.noteText.color = Color.yellow
            if self.iconaIisa is not None:
                self.iconaIisa.SetActive(True)
            if self.feedbackText is not None:
                self.feedbackText.text = "isa isa \n(" + format(frequency, ".1f") + " Hz)"
                self.feedbackText.color = Color.yellow

    def NascondiTutteLeIcone(self) -> None:
        if self.iconaIisa is not None:
            self.iconaIisa.SetActive(False)
        if self.iconaCala is not None:
            self.iconaCala.SetActive(False)
        if self.iconaPerfetto is not None:
            self.iconaPerfetto.SetActive(False)

    def OnAudioFilterRead(self, data: List[float], channels: int) -> None:
        for i in range(len(data)):
            data[i] = 0.0


# ============================================================
# MetronomeControllore.cs
# ============================================================


class MetronomeControllore(MonoBehaviour):
    def __init__(self):
        self.backgroundImage: Optional[Image] = None
        self.playButton: Optional[GameObject] = None
        self.pauseButton: Optional[GameObject] = None
        self.tickSource: Optional[AudioSource] = None
        self.defaultTickClip: Optional[AudioClip] = None
        self.alternativeTickClip: Optional[AudioClip] = None
        self.activeTickClip: Optional[AudioClip] = None
        self.bpm: int = 120
        self.isPlaying: bool = False
        self.nextTickTime: float = 0.0
        self.gameObject: GameObject = GameObject("MetronomeControllore")

    def Start(self) -> None:
        if self.defaultTickClip is None:
            self.CreaTickSintetico()
        self.activeTickClip = self.defaultTickClip

        if self.playButton is not None:
            self.playButton.SetActive(True)
        if self.pauseButton is not None:
            self.pauseButton.SetActive(False)

    def Update(self) -> None:
        if self.isPlaying:
            if AudioSettings.dspTime() >= self.nextTickTime:
                if self.tickSource is not None and self.activeTickClip is not None:
                    self.tickSource.PlayOneShot(self.activeTickClip)
                self.StartCoroutine(self.FlashBackground())
                self.nextTickTime += 60.0 / self.bpm

    def FlashBackground(self) -> Generator[Any, None, None]:
        if self.backgroundImage is not None:
            originale = self.backgroundImage.color
            self.backgroundImage.color = Color.white
            yield WaitForSeconds(0.05)
            self.backgroundImage.color = originale

    def CambiaSuono(self) -> None:
        if self.activeTickClip == self.defaultTickClip:
            if self.alternativeTickClip is not None:
                self.activeTickClip = self.alternativeTickClip
        else:
            self.activeTickClip = self.defaultTickClip

    def AvviaMetronomo(self) -> None:
        self.isPlaying = True
        self.nextTickTime = AudioSettings.dspTime()
        if self.playButton is not None:
            self.playButton.SetActive(False)
        if self.pauseButton is not None:
            self.pauseButton.SetActive(True)

    def FermaMetronomo(self) -> None:
        self.isPlaying = False
        if self.playButton is not None:
            self.playButton.SetActive(True)
        if self.pauseButton is not None:
            self.pauseButton.SetActive(False)

    def ImpostaBPM(self, nuovoValore: int) -> None:
        self.bpm = Mathf.Clamp(nuovoValore, 1, 999)
        if self.isPlaying:
            self.nextTickTime = AudioSettings.dspTime() + 60.0 / self.bpm

    def GetBPM(self) -> int:
        return self.bpm

    def ChiudiPannello(self) -> None:
        self.FermaMetronomo()
        self.gameObject.SetActive(False)

    def CreaTickSintetico(self) -> None:
        sampleFreq = 44100
        length = sampleFreq // 10
        self.defaultTickClip = AudioClip.Create("TickPerfetto", length, 1, sampleFreq, False)

        samples = [0.0] * length
        for i in range(length):
            samples[i] = Mathf.Sin(i * 2.0 * Mathf.PI * 800.0 / sampleFreq) * Mathf.Exp(-i * 0.05)
        self.defaultTickClip.SetData(samples, 0)


# ============================================================
# AnimazioneClickBottone.cs
# ============================================================


class AnimazioneClickBottone(MonoBehaviour):
    def __init__(self):
        self.scalaPremuto: float = 0.9
        self.velocita: float = 25.0
        self.scalaOriginale: Vector3 = Vector3.one
        self.scalaTarget: Vector3 = Vector3.one
        self.transform: Transform = Transform()

    def Start(self) -> None:
        self.scalaOriginale = self.transform.localScale
        self.scalaTarget = self.scalaOriginale

    def Update(self) -> None:
        self.transform.localScale = Mathf.Lerp(self.transform.localScale, self.scalaTarget, Time.deltaTime * self.velocita)

    def OnPointerDown(self, eventData: PointerEventData) -> None:
        self.scalaTarget = self.scalaOriginale * self.scalaPremuto

    def OnPointerUp(self, eventData: PointerEventData) -> None:
        self.scalaTarget = self.scalaOriginale

    def OnPointerExit(self, eventData: PointerEventData) -> None:
        self.scalaTarget = self.scalaOriginale


# ============================================================
# GestoreSplashScreen.cs
# ============================================================


class GestoreSplashScreen(MonoBehaviour):
    def __init__(self):
        self.immagineNonna: Optional[Image] = None
        self.immagineLogo: Optional[Image] = None
        self.yIniziale: float = 0.0
        self.yFinale: float = -500.0
        self.tempoIniziale: float = 1.5
        self.durataSfumaturaNonna: float = 1.5
        self.durataSpostamentoLogo: float = 1.2
        self.tempoLogoFermo: float = 1.0
        self.durataSfumaturaLogo: float = 1.0
        self.tempoSchermoNero: float = 0.5
        self.nomeScenaGioco: str = "MenuPrincipale"

    def Start(self) -> None:
        if self.immagineLogo is not None:
            rectLogo = self.immagineLogo.GetComponent(RectTransform)
            rectLogo.anchoredPosition = Vector2(rectLogo.anchoredPosition.x, self.yIniziale)
        self.StartCoroutine(self.SequenzaAnimazione())

    def SequenzaAnimazione(self) -> Generator[Any, None, None]:
        yield WaitForSeconds(self.tempoIniziale)

        tNonna = 0.0
        coloreNonna = self.immagineNonna.color if self.immagineNonna is not None else Color.white
        while tNonna < self.durataSfumaturaNonna:
            tNonna += Time.deltaTime
            alpha = Mathf.Lerp(1.0, 0.0, tNonna / self.durataSfumaturaNonna)
            if self.immagineNonna is not None:
                self.immagineNonna.color = Color(coloreNonna.r, coloreNonna.g, coloreNonna.b, alpha)
            yield None

        tSposta = 0.0
        rectLogo = self.immagineLogo.GetComponent(RectTransform) if self.immagineLogo is not None else RectTransform()
        posPartenza = Vector2(rectLogo.anchoredPosition.x, self.yIniziale)
        posArrivo = Vector2(rectLogo.anchoredPosition.x, self.yFinale)

        while tSposta < self.durataSpostamentoLogo:
            tSposta += Time.deltaTime
            progress = tSposta / self.durataSpostamentoLogo
            progress = progress * progress * (3.0 - 2.0 * progress)
            rectLogo.anchoredPosition = Mathf.Lerp(posPartenza, posArrivo, progress)
            yield None
        rectLogo.anchoredPosition = posArrivo

        yield WaitForSeconds(self.tempoLogoFermo)

        tLogo = 0.0
        coloreLogo = self.immagineLogo.color if self.immagineLogo is not None else Color.white
        while tLogo < self.durataSfumaturaLogo:
            tLogo += Time.deltaTime
            alpha = Mathf.Lerp(1.0, 0.0, tLogo / self.durataSfumaturaLogo)
            if self.immagineLogo is not None:
                self.immagineLogo.color = Color(coloreLogo.r, coloreLogo.g, coloreLogo.b, alpha)
            yield None

        yield WaitForSeconds(self.tempoSchermoNero)
        SceneManager.LoadScene(self.nomeScenaGioco)
