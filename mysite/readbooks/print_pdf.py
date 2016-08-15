from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from readbooks import models
class MyPrint:
	def __init__(self, buffer, pagesize):
		self.buffer = buffer
		if pagesize=='A4':
			self.pagesize = A4
		self.width, self.height = self.pagesize

	def print_review(self, review_id):

		buffer = self.buffer
		document = SimpleDocTemplate(buffer,rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=72, pagesize=self.pagesize)
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
		element = []
		review_to_pdf = models.Review.objects.get(id=review_id)
		# element.append(Paragraph(review_to_pdf.review_heading, styles['Heading1']))
		element.append(Paragraph(review_to_pdf.review), styles['Normal'])
		document.build(element)
		pdf = buffer.getvalue()
		buffer.close()
		return pdf
