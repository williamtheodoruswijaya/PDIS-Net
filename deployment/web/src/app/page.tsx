"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import ResultView from "@/components/ResultView";
import { listModels, predict, type ModelInfo, type Prediction } from "@/lib/api/client";
import styles from "./page.module.css";

const ARCH_NAMES: Record<string, string> = {
  segformer: "SegFormer",
  unet: "U-Net",
  deeplab: "DeepLabV3+",
};
const BACKBONE_NAMES: Record<string, string> = {
  mit_b0: "MiT-B0",
  mit_b3: "MiT-B3",
  mit_b5: "MiT-B5",
  resnet34: "ResNet-34",
  resnet50: "ResNet-50",
  resnet101: "ResNet-101",
};
const INIT_NAMES: Record<string, string> = {
  raw: "None (from scratch)",
  imagenet: "ImageNet",
  aerial: "Aerial (tree canopy)",
  ade: "ADE20K",
  drone: "Drone",
};
const LEVEL_NAMES: Record<string, string> = {
  none: "None",
  low: "Low",
  moderate: "Moderate",
  high: "High",
};

const COVERAGE_SCALE = 10;
const CUT_OFFS = [1.1, 4.5];

type Choice = { arch: string; backbone: string; init: string };

const DEFAULT_CHOICE: Choice = { arch: "segformer", backbone: "mit_b3", init: "imagenet" };

export default function Dashboard() {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [choice, setChoice] = useState<Choice>(DEFAULT_CHOICE);
  const [photo, setPhoto] = useState<File | null>(null);
  const [result, setResult] = useState<Prediction | null>(null);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  const fileInput = useRef<HTMLInputElement>(null);
  const latestRequest = useRef(0);

  const photoUrl = useMemo(() => (photo ? URL.createObjectURL(photo) : null), [photo]);

  useEffect(() => {
    listModels()
      .then(setModels)
      .catch(() => setError("Cannot reach the server. It may be waking up, refresh in a minute."));
  }, []);

  const archs = unique(models.map((m) => m.arch));
  const backbones = unique(models.filter((m) => m.arch === choice.arch).map((m) => m.backbone));
  const inits = models.filter((m) => m.arch === choice.arch && m.backbone === choice.backbone);

  async function analyse(newPhoto: File | null, newChoice: Choice) {
    if (!newPhoto) return;

    const request = ++latestRequest.current;
    setStatus("Analysing...");
    setError("");

    try {
      const answer = await predict(newPhoto, newChoice.arch, newChoice.backbone, newChoice.init);
      if (request !== latestRequest.current) return;
      setResult(answer);
    } catch (e) {
      if (request !== latestRequest.current) return;
      setError((e as Error).message);
    }
    setStatus("");
  }

  function choose(newChoice: Choice) {
    setChoice(newChoice);
    analyse(photo, newChoice);
  }

  function pickArch(arch: string) {
    const top = best(models.filter((m) => m.arch === arch));
    choose({ arch, backbone: top.backbone, init: top.init });
  }

  function pickBackbone(backbone: string) {
    const top = best(models.filter((m) => m.arch === choice.arch && m.backbone === backbone));
    choose({ ...choice, backbone, init: top.init });
  }

  function pickInit(init: string) {
    choose({ ...choice, init });
  }

  function pickPhoto(file: File | undefined) {
    if (!file) return;
    setPhoto(file);
    setResult(null);
    analyse(file, choice);
  }

  return (
    <>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <h1>Plastic Waste Monitoring Dashboard</h1>
        </div>
      </header>

      <main className={styles.page}>
        <div className={styles.columns}>
          <section className={styles.left}>
            <div className={styles.panel}>
              <div className={styles.modelPicker}>
                <label>
                  Model
                  <select value={choice.arch} onChange={(e) => pickArch(e.target.value)}>
                    {archs.map((arch) => (
                      <option key={arch} value={arch}>
                        {ARCH_NAMES[arch] ?? arch}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  Backbone
                  <select value={choice.backbone} onChange={(e) => pickBackbone(e.target.value)}>
                    {backbones.map((backbone) => (
                      <option key={backbone} value={backbone}>
                        {BACKBONE_NAMES[backbone] ?? backbone}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  Pretrained weights
                  <select value={choice.init} onChange={(e) => pickInit(e.target.value)}>
                    {inits.map((m) => (
                      <option key={m.init} value={m.init}>
                        {INIT_NAMES[m.init] ?? m.init} (mIoU {m.miou.toFixed(3)})
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <button className={styles.uploadButton} onClick={() => fileInput.current?.click()}>
                Upload Image
              </button>
              <input
                ref={fileInput}
                type="file"
                accept="image/jpeg,image/png"
                hidden
                onChange={(e) => pickPhoto(e.target.files?.[0])}
              />
            </div>

            <div className={styles.panel}>
              <p className={styles.panelTitle}>Photo</p>
              {photoUrl ? (
                <img className={styles.image} src={photoUrl} alt="Uploaded aerial photo" />
              ) : (
                <div className={styles.emptyPhoto}>No photo yet</div>
              )}
            </div>

            <div className={styles.panel}>
              <ResultView photoUrl={photoUrl} maskB64={result?.mask_png_b64 ?? null} />
            </div>
          </section>

          <section className={styles.right}>
            <div className={styles.cards}>
              <div className={`${styles.card} ${result ? styles[`level_${result.level}`] : ""}`}>
                Category
                <strong>{result ? LEVEL_NAMES[result.level] : "-"}</strong>
              </div>
              <div className={styles.card}>
                How Much Plastic Coverage
                <strong>{result ? `${result.coverage_pct}%` : "-"}</strong>
                <div className={styles.bar}>
                  <div
                    className={styles.barFill}
                    style={{ width: `${Math.min((result?.coverage_pct ?? 0) / COVERAGE_SCALE, 1) * 100}%` }}
                  />
                  {CUT_OFFS.map((cut) => (
                    <i key={cut} className={styles.tick} style={{ left: `${(cut / COVERAGE_SCALE) * 100}%` }} />
                  ))}
                </div>
                <div className={styles.tickLabels}>
                  {CUT_OFFS.map((cut) => (
                    <span key={cut} style={{ left: `${(cut / COVERAGE_SCALE) * 100}%` }}>
                      {cut}%
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className={styles.recommendation}>
              <h2>Recommendation</h2>
              {result ? (
                <p>{result.recommendation}</p>
              ) : (
                <p className={styles.placeholder}>Upload a photo to get a recommendation.</p>
              )}
            </div>

            {status && <p className={styles.status}>{status}</p>}
            {error && <p className={styles.error}>{error}</p>}

            {result && (
              <p className={styles.note}>
                Category compares this photo&apos;s plastic coverage with the 1,474 FloPWD photos that contain
                plastic (bottom, middle or top third). It is not a water-quality rating. Model {result.model},{" "}
                {result.inference_ms} ms.
              </p>
            )}
          </section>
        </div>
      </main>
    </>
  );
}

function unique(values: string[]) {
  return [...new Set(values)];
}

function best(rows: ModelInfo[]) {
  return rows.reduce((top, row) => (row.miou > top.miou ? row : top));
}
