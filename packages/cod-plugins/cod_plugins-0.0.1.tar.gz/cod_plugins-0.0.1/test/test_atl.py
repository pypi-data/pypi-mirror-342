from pdf_generator import PDFGenerator


def test_generate():
    # config = {
    #     "url": "https://agricod.fujitsu-systems-europe.com/",
    #     "title_text": "Advanced Technology Laboratories - Quality Environmental Testing",
    #     "graph_selection_mode": "classification"
    # }

    zip_input_path = "/data/ATL/tests/batch_67fd422061eb8471363c9d8f_dump.zip"
    output_folder = "/data/ATL/tests"

    # before
    # pdf_generator_before = PDFGenerator(zip_input_path=zip_input_path, output_folder=output_folder,
    #                                     title_text="Advanced Technology Laboratories - Quality Environmental Testing",
    #                                     graph_selection_mode="classification",
    #                                     url="https://agricod.fujitsu-systems-europe.com/",
    #                                     log_level="INFO")
    # pdf_generator_before.generate_report()

    # after
    plugin_conf = {
        "forced_output_location": "/tmp/",
        "special_atl": True
    }
    pdf_generator_after = PDFGenerator(zip_input_path=zip_input_path, output_folder=output_folder,
                                       title_text="Advanced Technology Laboratories - Quality Environmental Testing",
                                       graph_selection_mode="validation",
                                       url="https://agricod.fujitsu-systems-europe.com/",
                                       log_level="INFO",
                                       **plugin_conf)
    pdf_generator_after.generate_report()
