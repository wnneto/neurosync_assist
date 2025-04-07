// components/VideoLinkButton.jsx
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { gerarLinkTelemedicina } from "@/services/consultas";

export default function VideoLinkButton({ consultaId }) {
  const [link, setLink] = useState(null);
  const [loading, setLoading] = useState(false);

  const gerarLink = async () => {
    setLoading(true);
    try {
      await gerarLinkTelemedicina(consultaId);
      const generatedLink = `https://meet.jit.si/consulta_${consultaId}`;
      setLink(generatedLink);
      alert("✅ Link gerado com sucesso!");
    } catch (err) {
      alert("Erro ao gerar link.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-2">
      <Button onClick={gerarLink} disabled={loading} className="w-full">
        {loading ? "Gerando..." : "🔗 Gerar Link de Vídeo"}
      </Button>
      {link && (
        <p className="text-sm break-all">
          Link: <a href={link} target="_blank" className="text-blue-600 underline">{link}</a>
        </p>
      )}
    </div>
  );
}
