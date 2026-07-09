from html2image import Html2Image
import os

hti = Html2Image(size=(800, 1000))

html_file_path = r'd:\Diplom1\tabriknoma.html'
output_dir = r'd:\Diplom1'

hti.output_path = output_dir

hti.screenshot(
    html_file=html_file_path,
    save_as='tabriknoma.png'
)

print(r"Screenshot saved as d:\Diplom1\tabriknoma.png")
