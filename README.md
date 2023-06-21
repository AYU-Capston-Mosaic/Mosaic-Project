
# Implementation of AI-based Sensitive Content Masking System in Public Administrative Documents

## Abstract 
> When public administrative documents are submitted to public institutions, personal information leakage occurs within institutions or companies frequently as news articles. In fact, personal information protection is not properly implemented in reality because public officials in public institutions manage documents and accidentally or deliberately leak personal information of civil petitioners. This study introduces a research to improve the decline in Hangul recognition rate in OCR programs provided as open source. We present solutions by adjusting the attribute values of OCR libraries and improving them through performance comparisons, or by designing machine learning model algorithms to increase accuracy. It also presents a method for visualization processing for recognized character part for the mosaic service. We established a mosaic processing method according to user-specified selection for the personal information content that needs to be selected for visualization processing and a service direction for improving the bounding box accuracy, and lastly built an AI-based service model suitable for this. In this paper, we can increase the level of personal information protection through mosaic of documents and photos using AI-based OCR function, and it is possible to mosaic personal information that has not been recognized yet. In addition, work efficiency can be improved by simplifying the processing process through automation of the manual mosaic work.

<br>
<br>

---

## Project Version

- python 3.9.16
  - OpenCV is not functioning properly in the Python upper version!
  - _Please install the 3.9.16 version._

<br>
<br>

---

## How to Run
```bash
>> git clone https://github.com/Mosaicec/Mosaicec.git
>> cd Mosaicec
>> python3 -m venv .venv
>> cd .venv
>> source bin/activate
>> cp -r ../mosaicec .
>> cd mosaicec
>> sh mosaicec.sh
```
