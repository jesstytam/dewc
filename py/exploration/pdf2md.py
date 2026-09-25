from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser

config = {
    "diable_orc": True,
    "mode": "fast",
    "use_pdftext_reading_order": True,
    # "min_recon_score": 0.75,
    "html_tables_in_markdown": True,
    "paginate_output": True,
    "page_separator": "<!-- PAGE BREAK -->",
    "output_dir": "data/papers/md",
    "output_format": "markdown"
}
config_parser = ConfigParser(config)

converter = PdfConverter(
    config=config_parser.generate_config_dict(),
    artifact_dict=create_model_dict(),
    processor_list=config_parser.get_processors(),
    renderer=config_parser.get_renderer(),
    # llm_service=config_parser.get_llm_service(),
)
rendered = converter("data/papers/pdf/29339.pdf")