"""
===============================================================================
VERSIONE PYTHON UNIFICATA - SCOPO DIDATTICO
-------------------------------------------------------------------------------
Questa NON e' una conversione 1:1 eseguibile in Unity.
Serve per una lezione teorica, quindi l'obiettivo e' mostrare:
- come si traduce la logica C# in Python;
- come si separano responsabilita e componenti;
- come si descrive il flusso di un'app musicale/interattiva.

Il codice usa classi Python semplici e commenti estesi.
Le parti Unity-specifiche (scene, coroutine reali, UI reale, AudioSource reale,
input touch reale) sono simulate con metodi e stampe.
===============================================================================
"""

from dataclasses import dataclass, field
from math import log2, pow
from typing import List, Optional


# ============================================================================
# 1) RULLO NUMERICO
# ----------------------------------------------------------------------------
# In Unity il rullo e' un componente UI scrollabile.
# In Python lo semplifichiamo come una lista di valori e un indice corrente.
# ============================================================================
@dataclass
class ControlloreRullo:
    nome: str
    valori: List[int] = field(default_factory=lambda: list(range(10)))
    indice_corrente: int = 0

    def seleziona_indice(self, indice: int) -> None:
        """Seleziona un indice del rullo simulando lo snapping sul valore scelto."""
        self.indice_corrente = indice % len(self.valori)
        print(f"[{self.nome}] selezionato indice {self.indice_corrente} -> valore {self.valore_selezionato}")

    @property
    def valore_selezionato(self) -> int:
        """Restituisce il valore numerico attualmente selezionato."""
        return self.valori[self.indice_corrente]


# ============================================================================
# 2) METRONOMO
# ----------------------------------------------------------------------------
# In Unity c'e audio in tempo reale e gestione del DSP clock.
# Qui manteniamo solo stato, BPM e descrizione del comportamento.
# ============================================================================
@dataclass
class MetronomeControllore:
    bpm: int = 120
    is_playing: bool = False
    suono_attivo: str = "default"

    def imposta_bpm(self, nuovo_valore: int) -> None:
        """Aggiorna il BPM con un limite di sicurezza tra 1 e 999."""
        self.bpm = max(1, min(999, nuovo_valore))
        print(f"[Metronomo] BPM impostato a {self.bpm}")

    def avvia_metronomo(self) -> None:
        """Simula l'avvio del metronomo."""
        self.is_playing = True
        print(f"[Metronomo] Avviato a {self.bpm} BPM")

    def ferma_metronomo(self) -> None:
        """Simula l'arresto del metronomo."""
        self.is_playing = False
        print("[Metronomo] Fermato")

    def cambia_suono(self) -> None:
        """Alterna fra due tipi di tick."""
        self.suono_attivo = "alternativo" if self.suono_attivo == "default" else "default"
        print(f"[Metronomo] Suono attivo: {self.suono_attivo}")

    def tick(self) -> None:
        """Simula un singolo tick del metronomo."""
        if self.is_playing:
            print(f"[Metronomo] TICK ({self.suono_attivo}) @ {self.bpm} BPM")


# ============================================================================
# 3) GESTORE BPM TOTALE
# ----------------------------------------------------------------------------
# Legge i tre rulli e costruisce il numero finale del metronomo.
# ============================================================================
@dataclass
class GestoreTotaleBpm:
    metronomo: MetronomeControllore
    rullo_centinaia: ControlloreRullo
    rullo_decine: ControlloreRullo
    rullo_unita: ControlloreRullo
    bpm_attuale: int = -1

    def aggiorna(self) -> None:
        """Calcola il BPM totale e lo invia al metronomo se cambia."""
        nuovo_bpm = (
            self.rullo_centinaia.valore_selezionato * 100
            + self.rullo_decine.valore_selezionato * 10
            + self.rullo_unita.valore_selezionato
        )

        if nuovo_bpm < 1:
            nuovo_bpm = 1

        if nuovo_bpm != self.bpm_attuale:
            self.bpm_attuale = nuovo_bpm
            self.metronomo.imposta_bpm(nuovo_bpm)


# ============================================================================
# 4) ACCORDATORE
# ----------------------------------------------------------------------------
# In Unity la frequenza arriva da microfono + FFT.
# (La Fast Fourier Transform serve a calcolare in modo veloce la trasformata di Fourier, per riconoscere in modo preciso quali frequenze ci siano nel segnale registrato e quanto siano forti).
# Qui per fini didattici passiamo direttamente una frequenza in input.
# ============================================================================
@dataclass
class GuitarTuner:
    notes: List[str] = field(default_factory=lambda: ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])

    def analizza_frequenza(self, frequency: float) -> dict:
        """
        Converte una frequenza nella nota piu vicina e restituisce un feedback.
        Formula base:
            note_index = round(12 * log2(f / 440) + 69)
        dove 440 Hz = A4.
        """
        if frequency <= 0:
            return {"errore": "Frequenza non valida"}

        note_index = round(12 * log2(frequency / 440.0) + 69)
        note_name = self.notes[note_index % 12]
        target_freq = 440.0 * pow(2.0, (note_index - 69) / 12.0)
        diff = frequency - target_freq

        if abs(diff) < 1.0:
            stato = "accordata"
            messaggio = "A posto!"
            colore = "verde"
            icona = "pollice_su"
        elif diff > 0:
            stato = "troppo alta"
            messaggio = "abbassa un po'"
            colore = "arancione"
            icona = "freccia_giu"
        else:
            stato = "troppo bassa"
            messaggio = "alza, alza!"
            colore = "giallo"
            icona = "freccia_su"

        risultato = {
            "frequenza": round(frequency, 2),
            "nota": note_name,
            "target_freq": round(target_freq, 2),
            "differenza": round(diff, 2),
            "stato": stato,
            "messaggio": messaggio,
            "colore": colore,
            "icona": icona,
        }
        print(f"[Tuner] {risultato}")
        return risultato


# ============================================================================
# 5) ANIMAZIONE CLICK BOTTONE
# ----------------------------------------------------------------------------
# In Unity si lavora sulla scala del transform.
# Qui mostriamo solo lo stato logico della pressione.
# ============================================================================
@dataclass
class AnimazioneClickBottone:
    scala_originale: float = 1.0
    scala_premuto: float = 0.9
    scala_target: float = 1.0

    def on_pointer_down(self) -> None:
        self.scala_target = self.scala_premuto
        print(f"[Bottone] premuto -> scala target {self.scala_target}")

    def on_pointer_up(self) -> None:
        self.scala_target = self.scala_originale
        print(f"[Bottone] rilasciato -> scala target {self.scala_target}")

    def on_pointer_exit(self) -> None:
        self.scala_target = self.scala_originale
        print(f"[Bottone] uscita dito -> scala target {self.scala_target}")


# ============================================================================
# 6) SPLASH SCREEN
# ----------------------------------------------------------------------------
# In Unity ci sono coroutine e animazioni temporizzate.
# In Python descriviamo i passaggi come sequenza testuale.
# ============================================================================
@dataclass
class GestoreSplashScreen:
    tempo_iniziale: float = 1.5
    durata_sfumatura_nonna: float = 1.5
    durata_spostamento_logo: float = 1.2
    tempo_logo_fermo: float = 1.0
    durata_sfumatura_logo: float = 1.0
    tempo_schermo_nero: float = 0.5
    nome_scena_gioco: str = "MenuPrincipale"

    def esegui_sequenza(self) -> None:
        print("[Splash] Attesa iniziale")
        print("[Splash] Dissolvenza immagine iniziale")
        print("[Splash] Spostamento logo")
        print("[Splash] Pausa logo fermo")
        print("[Splash] Dissolvenza logo")
        print(f"[Splash] Caricamento scena: {self.nome_scena_gioco}")


# ============================================================================
# 7) APP PRINCIPALE
# ----------------------------------------------------------------------------
# Questa classe mostra come i moduli si combinano in un unico sistema.
# ============================================================================
class AppMusicaleDidattica:
    def __init__(self) -> None:
        self.metronomo = MetronomeControllore()

        self.rullo_centinaia = ControlloreRullo(nome="Centinaia")
        self.rullo_decine = ControlloreRullo(nome="Decine")
        self.rullo_unita = ControlloreRullo(nome="Unita")

        self.gestore_bpm = GestoreTotaleBpm(
            metronomo=self.metronomo,
            rullo_centinaia=self.rullo_centinaia,
            rullo_decine=self.rullo_decine,
            rullo_unita=self.rullo_unita,
        )

        self.tuner = GuitarTuner()
        self.animazione_bottone = AnimazioneClickBottone()
        self.splash = GestoreSplashScreen()

    def demo(self) -> None:
        """Esegue una piccola dimostrazione del flusso applicativo."""
        print("\n=== DEMO APP MUSICALE DIDATTICA ===")

        # Splash screen iniziale
        self.splash.esegui_sequenza()

        # Impostazione BPM tramite tre rulli
        self.rullo_centinaia.seleziona_indice(1)  # 1
        self.rullo_decine.seleziona_indice(2)     # 2
        self.rullo_unita.seleziona_indice(8)      # 8
        self.gestore_bpm.aggiorna()               # 128 BPM

        # Avvio metronomo
        self.metronomo.avvia_metronomo()
        self.metronomo.tick()
        self.metronomo.cambia_suono()
        self.metronomo.tick()

        # Simulazione accordatore
        self.tuner.analizza_frequenza(440.0)
        self.tuner.analizza_frequenza(445.0)
        self.tuner.analizza_frequenza(432.0)

        # Simulazione bottone
        self.animazione_bottone.on_pointer_down()
        self.animazione_bottone.on_pointer_up()

        # Stop metronomo
        self.metronomo.ferma_metronomo()


def main() -> None:
    app = AppMusicaleDidattica()
    app.demo()


if __name__ == "__main__":
    main()
