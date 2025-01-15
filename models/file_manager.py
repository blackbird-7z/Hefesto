import os
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from PyQt6.QtCore import QSettings

class FileManager:
    def __init__(self):
        self.files = []
        self.merged_files = []

        # Dicionário com formatos padrões e dimensões em milímetros (largura, altura)
        self.FORMAT_DIMENSIONS = {
            "A0": (841.0, 1189.0),
            "A1": (594.0, 841.0),
            "A2": (420.0, 594.0),
            "A3": (297.0, 420.0),
            "A4": (210.0, 297.0),
        }

        self.log_counters = {}

    def set_files(self, file_list):
        self.files = file_list

    def join_files_by_format(self):
        """
        Essa função junta os PDFs por formato, gera arquivos separados, e cria um logs.txt.
        Se o formato for A4 (ou A4_EXT), os arquivos serão mesclados em um único PDF,
        adicionando 2 páginas em branco ENTRE cada arquivo.
        """

        # Reinicializa os contadores e a lista de PDFs mesclados
        self.log_counters = {}
        self.merged_files = []

        # Determinar o diretório de destino com base em QSettings
        settings = QSettings("MHA", "Hefesto")
        sequence = int(settings.value("sequence", 1))
        folder_name = f"he_{sequence:03d}"
        settings.setValue("sequence", sequence + 1)

        download_path = Path(os.path.expanduser("~/Downloads"))
        dest_path = download_path / folder_name
        dest_path.mkdir(parents=True, exist_ok=True)

        # Dicionário que agrupa por (formato, menor_dim, maior_dim)
        format_groups = {}

        # 1) Agrupa arquivos
        for pdf_file in self.files:
            pdf_file = Path(pdf_file)
            if pdf_file.exists() and pdf_file.suffix.lower() == '.pdf':
                formato, dims = self.identify_format_and_dims(pdf_file)

                # (A) Atualiza o contador do formato
                if formato not in self.log_counters:
                    self.log_counters[formato] = 0
                self.log_counters[formato] += 1

                # (B) Agrupa no dict
                menor_dim = round(dims[0])
                maior_dim = round(dims[1])
                key = (formato, menor_dim, maior_dim)
                if key not in format_groups:
                    format_groups[key] = []
                format_groups[key].append(pdf_file)

        # 2) Junta os PDFs de cada chave
        format_counters = {} 
        
        for key, arquivos in format_groups.items():
            formato, menor_dim, maior_dim = key

            if arquivos:
                writer = PdfWriter()
                mm_to_points = 2.834645
                width_pt = menor_dim * mm_to_points
                height_pt = maior_dim * mm_to_points

                for i, arquivo in enumerate(arquivos):
                    reader = PdfReader(str(arquivo))
                    for page in reader.pages:
                        writer.add_page(page)

                    # Se for A4 / A4_EXT, insere 2 páginas em branco se não for o último PDF
                    if (formato in ("A4", "A4_EXT")) and (i < len(arquivos) - 1):
                        writer.add_blank_page(width=width_pt, height=height_pt)
                        writer.add_blank_page(width=width_pt, height=height_pt)

                # 3) Define o nome do arquivo final
                if "Desconhecido" in formato:
                    # Para formatos desconhecidos => "FormatoDesconhecido-1.pdf", etc.
                    base_name = "FormatoDesconhecido"
                elif "EXT" in formato:
                    # Para formatos EXT => "A0_EXT-1.pdf", etc.
                    base_name = formato
                else:
                    # Formatos padrão => "A0.pdf", "A1.pdf", etc.
                    base_name = formato

                # Se for "FormatoDesconhecido" ou EXT => numerar
                if base_name == "FormatoDesconhecido" or "EXT" in base_name:
                    if base_name not in format_counters:
                        format_counters[base_name] = 1
                    else:
                        format_counters[base_name] += 1
                    merged_filename = f"{base_name}-{format_counters[base_name]}.pdf"
                else:
                    # Formato padrão, sem numeração
                    merged_filename = f"{base_name}.pdf"

                merged_path = dest_path / merged_filename
                with open(merged_path, "wb") as f:
                    writer.write(f)
                self.merged_files.append(merged_path)

        # 4) Cria o arquivo de log
        self._write_logs(dest_path)

    def identify_format_and_dims(self, pdf_path: Path):
        """
        Essa função identifica o formato do PDF e também retorna as dimensões ordenadas (menor, maior).
        Se for desconhecido, retorna ("Desconhecido", dims).
        """
        POINT_TO_MM = 0.352777
        TOLERANCIA_PADRAO = 5.0
        LIMITE_EXTENSO = 50.0

        reader = PdfReader(str(pdf_path))
        if len(reader.pages) > 0:
            page = reader.pages[0]
            width_pt = float(page.mediabox.width)
            height_pt = float(page.mediabox.height)

            width_mm = width_pt * POINT_TO_MM
            height_mm = height_pt * POINT_TO_MM

            dims_pdf = sorted([width_mm, height_mm])

            for fmt_name, (w_mm, h_mm) in self.FORMAT_DIMENSIONS.items():
                dims_fmt = sorted([w_mm, h_mm])
                menor_fmt, maior_fmt = dims_fmt
                menor_pdf, maior_pdf = dims_pdf

                # Formato padrão dentro da tolerância
                if (abs(menor_pdf - menor_fmt) <= TOLERANCIA_PADRAO and
                    abs(maior_pdf - maior_fmt) <= TOLERANCIA_PADRAO):
                    return (fmt_name, dims_pdf)

                # Formato estendido?
                if abs(menor_pdf - menor_fmt) <= TOLERANCIA_PADRAO:
                    if maior_pdf > (maior_fmt + LIMITE_EXTENSO):
                        return (fmt_name + "_EXT", dims_pdf)
                if abs(maior_pdf - maior_fmt) <= TOLERANCIA_PADRAO:
                    if menor_pdf > (menor_fmt + LIMITE_EXTENSO):
                        return (fmt_name + "_EXT", dims_pdf)

            # Não achou formato padrão/EXT => desconhecido
            return ("Desconhecido1", dims_pdf)

        # Se não há páginas, algo está errado, considerar desconhecido
        return ("Desconhecido1", (0, 0))

    def _write_logs(self, dest_path: Path):
        """
        Essa função cria um arquivo logs.txt no diretório de destino
        com a quantidade de arquivos processados para cada formato.
        """
        log_file = dest_path / "logs.txt"
        sorted_formats = sorted(self.log_counters.keys())

        col1_width = 21
        col2_width = 24

        horizontal_line = (
            "+" + "-" * (col1_width + 2) +
            "+" + "-" * (col2_width + 2) + "+\n"
        )

        with open(log_file, "w", encoding="utf-8") as f:
            f.write("    ======= LOG DE ARQUIVOS POR FORMATO =======\n\n")
            f.write(horizontal_line)
            header = (
                "| "
                + "Formato de arquivos".ljust(col1_width)
                + " | "
                + "Quantidade de arquivos".ljust(col2_width)
                + " |\n"
            )
            f.write(header)
            f.write(horizontal_line)

            for formato in sorted_formats:
                quantidade_str = str(self.log_counters[formato])
                line = (
                    "| "
                    + formato.ljust(col1_width)
                    + " | "
                    + quantidade_str.ljust(col2_width)
                    + " |\n"
                )
                f.write(line)

            f.write(horizontal_line)
