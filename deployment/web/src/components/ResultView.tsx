"use client";

import { useState } from "react";

import styles from "./ResultView.module.css";

type Mode = "mask" | "overlay";

const MODES: { value: Mode; label: string }[] = [
  { value: "mask", label: "Mask" },
  { value: "overlay", label: "Overlay" },
];

export default function ResultView({ photoUrl, maskB64 }: { photoUrl: string | null; maskB64: string | null }) {
  const [mode, setMode] = useState<Mode>("mask");
  const maskUrl = maskB64 ? `data:image/png;base64,${maskB64}` : null;

  return (
    <>
      <div className={styles.top}>
        <p className={styles.title}>Result</p>
        <div className={styles.toggle} role="group" aria-label="Result view">
          {MODES.map((m) => (
            <button
              key={m.value}
              className={mode === m.value ? styles.active : ""}
              aria-pressed={mode === m.value}
              onClick={() => setMode(m.value)}
            >
              {m.label}
            </button>
          ))}
        </div>
      </div>

      {!maskUrl && <div className={styles.empty}>Upload a photo to see the plastic mask</div>}

      {maskUrl && mode === "mask" && (
        <img className={styles.image} src={maskUrl} alt="Plastic mask: white is plastic, black is everything else" />
      )}

      {maskUrl && mode === "overlay" && photoUrl && (
        <div className={styles.overlay}>
          <img className={styles.image} src={photoUrl} alt="Uploaded photo with the detected plastic highlighted in red" />
          <div className={styles.highlight} style={{ maskImage: `url(${maskUrl})` }} />
        </div>
      )}

      {mode === "mask" ? (
        <div className={styles.legend}>
          <span>
            <i className={styles.swatch} style={{ background: "#fff" }} /> Plastic
          </span>
          <span>
            <i className={styles.swatch} style={{ background: "#111" }} /> Non-Plastic
          </span>
        </div>
      ) : (
        <div className={styles.legend}>
          <span>
            <i className={`${styles.swatch} ${styles.swatchPlastic}`} /> Plastic
          </span>
          <span>Everything else = the original photo</span>
        </div>
      )}
    </>
  );
}
