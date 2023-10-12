from parsers import jsonlines_iterator_parser, one_file_parser, folder_parser
from outputs import save_html_data, save_json_data

output = one_file_parser("input/test.docx")
#output = folder_parser("input")

save_html_data(output)
save_json_data(output)
