from pdf_generator import PDFGenerator

def test_generate():
    # zip_input_path = "/nas/shared/Data/AgriParadigma/dumps/batch_656f5a680455154ec43cf040_dump.zip"
    # output_folder = "/nas/shared/Data/AgriParadigma/pdf"

    # zip_input_path = "/nas/shared/Data/AgriParadigma/dumps/batch_656f59480455154ec43cdf39_dump.zip"
    # output_folder = "/nas/shared/Data/AgriParadigma/pdf"

    zip_input_path = "/nas/shared/Data/AgriParadigma/dumps/batch_656f59a00455154ec43ce3ed_dump.zip"
    output_folder = "/nas/shared/Data/AgriParadigma/pdf/test"

    pdf_generator = PDFGenerator(zip_input_path=zip_input_path, output_folder = output_folder, graph_selection_mode="classification", 
                                 url="https://agricod.demo3.fujitsu-systems-europe.com/alphacod_expert/", log_level="INFO")
    pdf_generator.generate_report()