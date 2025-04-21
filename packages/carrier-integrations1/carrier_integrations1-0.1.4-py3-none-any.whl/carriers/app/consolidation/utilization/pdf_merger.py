from io import BytesIO

from pypdf import PdfWriter, PdfReader

from app.consolidation.utilization.s3_aws_ops import SimpleStorageS3

"""
merge pdf from byte data
"""


def pdf_merge_from_byte(data, order_id, tracking_number):
    """

    :param data:
    :param order_id:
    :param tracking_number:
    :return:
    """
    output = PdfWriter()
    outputStream = BytesIO()
    for f in data:
        pdf_content = BytesIO(f)
        input_data = PdfReader(pdf_content, strict=False)
        output.append(input_data)  # for i in range(len(input_data.pages)):  #     output.add_page(input_data.pages[i])  # .rotateClockwise(rotate))

    output.write(outputStream)
    _link = SimpleStorageS3(outputStream.getvalue(),True, str(tracking_number or ''), order_id)
    output.close()
    outputStream.close()
    return _link  # with open('%s_%s.pdf' % (order_id, tracking_number), 'wb') as fp:  #         fp.write(outputStream.getvalue())

    # return ''
