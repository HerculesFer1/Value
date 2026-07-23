/**
 * App — casca inicial da interface (esqueleto Fase 6).
 *
 * A casca respira, o dado é compacto (PROMPT_VALUE.md §11). O fluxo completo
 * (ingestão → emissão) e a faixa de proveniência funcional entram na Fase 6.
 * Aqui fica apenas a moldura e uma demonstração do elemento-assinatura.
 */
import { useState } from "react";

export function App() {
  return (
    <div style={{ minHeight: "100%", display: "flex", flexDirection: "column" }}>
      <header
        style={{
          padding: "var(--e-4) var(--e-5)",
          borderBottom: "1px solid var(--fio)",
          background: "var(--superficie-elevada)",
        }}
      >
        <div style={{ fontSize: "var(--t-22)", fontWeight: 600 }}>value</div>
        <div style={{ fontSize: "var(--t-13)", color: "var(--texto-secundario)" }}>
          memoriais de cálculo — uso interno
        </div>
      </header>

      <main style={{ padding: "var(--e-5)", flex: 1 }}>
        <section
          style={{
            background: "var(--superficie-elevada)",
            border: "1px solid var(--fio)",
            borderRadius: "var(--raio-cartao)",
            boxShadow: "var(--sombra-cartao)",
            padding: "var(--e-4)",
            maxWidth: 720,
          }}
        >
          <h1 style={{ fontSize: "var(--t-17)", fontWeight: 600, margin: 0 }}>
            scaffold pronto
          </h1>
          <p style={{ fontSize: "var(--t-15)", color: "var(--texto-secundario)" }}>
            o fluxo de ingestão a emissão será construído na fase 6. abaixo, uma
            amostra do elemento-assinatura: a faixa de proveniência.
          </p>

          <table style={{ borderCollapse: "collapse", marginTop: "var(--e-3)" }}>
            <tbody>
              <tr>
                <td style={{ padding: "var(--e-1) var(--e-3)" }}>2011</td>
                <td className="dado-financeiro" style={{ padding: "var(--e-1) var(--e-3)" }}>
                  2.302,32
                </td>
                <td style={{ padding: "var(--e-1) var(--e-3)" }}>
                  <FaixaProveniencia
                    dispositivo="sentença, item 3 do dispositivo"
                    norma="art. 1º-F Lei 9.494/97 (Tema 810/STF)"
                    serie="IPCA-E CJF Res. 990/2026 · v1 · hash a1b2c3"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}

/**
 * Faixa de proveniência: marcador discreto que abre um inspetor lateral (não
 * modal, separado por fio de cabelo) com a cadeia dispositivo → norma → série.
 * É a coisa que este produto faz e nenhum outro faz.
 */
function FaixaProveniencia({
  dispositivo,
  norma,
  serie,
}: {
  dispositivo: string;
  norma: string;
  serie: string;
}) {
  const [aberto, setAberto] = useState(false);
  return (
    <>
      <button
        onClick={() => setAberto((v) => !v)}
        aria-label="ver proveniência"
        style={{
          border: "1px solid var(--fio)",
          borderRadius: "var(--raio-campo)",
          background: "transparent",
          color: "var(--acento)",
          fontSize: "var(--t-11)",
          padding: "2px 6px",
          cursor: "pointer",
          transition: "var(--transicao)",
        }}
      >
        proveniência
      </button>

      {aberto && (
        <aside
          style={{
            position: "fixed",
            top: 0,
            right: 0,
            height: "100%",
            width: 360,
            background: "var(--superficie-elevada)",
            borderLeft: "1px solid var(--fio)",
            padding: "var(--e-4)",
            fontSize: "var(--t-13)",
          }}
        >
          <div style={{ fontWeight: 600, fontSize: "var(--t-15)" }}>proveniência</div>
          <Cadeia rotulo="dispositivo do título" valor={dispositivo} />
          <Cadeia rotulo="norma vigente na janela" valor={norma} />
          <Cadeia rotulo="ponto da série oficial" valor={serie} />
        </aside>
      )}
    </>
  );
}

function Cadeia({ rotulo, valor }: { rotulo: string; valor: string }) {
  return (
    <div style={{ marginTop: "var(--e-3)" }}>
      <div style={{ color: "var(--texto-secundario)", fontSize: "var(--t-11)" }}>
        {rotulo}
      </div>
      <div>{valor}</div>
    </div>
  );
}
