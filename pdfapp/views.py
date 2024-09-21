import PyPDF2
import pytesseract
from PIL import Image
from gtts import gTTS
from django.http import JsonResponse
from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def convert_pdf_to_voice(request):
    if request.method == 'POST':
        pdf_file: UploadedFile = request.FILES['pdf']
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Text extraction
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()

        # OCR in image-pdf cases
        if not text.strip():
            pdf_file.seek(0)
            image = Image.open(pdf_file)
            text = pytesseract.image_to_string(image)

        # Text to voice
        if text.strip():
            tts = gTTS(text=text, lang='es') # Spanish to test
            tts.save('output.mp3')  # Audio

            return JsonResponse({'message': 'PDF convertido a voz con éxito.'})

    return JsonResponse({'error': 'Error al procesar el archivo.'})
