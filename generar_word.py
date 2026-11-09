import zipfile
import os

content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="jpg" ContentType="image/jpeg"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

doc_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rIdImg1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/captura_blog.jpg"/>
</Relationships>"""

styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>
        <w:sz w:val="22"/>
        <w:szCs w:val="22"/>
        <w:lang w:val="es-MX"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="160" w:line="276" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>"""

def make_p(runs, align="left", space_before=0, space_after=160, hanging=0, left=0, border_bottom=False, shading=None):
    pPr = f'<w:pPr><w:jc w:val="{align}"/><w:spacing w:before="{space_before}" w:after="{space_after}" w:line="276" w:lineRule="auto"/>'
    if hanging or left:
        pPr += f'<w:ind w:left="{left}" w:hanging="{hanging}"/>'
    if border_bottom:
        pPr += '<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="0F3D5E"/></w:pBdr>'
    if shading:
        pPr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shading}"/>'
    pPr += '</w:pPr>'
    
    runs_xml = ""
    for text, bold, italic, color, size, underline in runs:
        rPr = '<w:rPr>'
        if bold:
            rPr += '<w:b/>'
        if italic:
            rPr += '<w:i/>'
        if underline:
            rPr += '<w:u w:val="single"/>'
        if color:
            rPr += f'<w:color w:val="{color}"/>'
        if size:
            rPr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        rPr += '</w:rPr>'
        escaped = (text.replace("&", "&amp;")
                       .replace("<", "&lt;")
                       .replace(">", "&gt;"))
        runs_xml += f'<w:r>{rPr}<w:t xml:space="preserve">{escaped}</w:t></w:r>'
    return f'<w:p>{pPr}{runs_xml}</w:p>'

def make_image_p(rel_id="rIdImg1", cx=5760000, cy=2610000):
    return f"""<w:p>
      <w:pPr>
        <w:jc w:val="center"/>
        <w:spacing w:before="160" w:after="220"/>
      </w:pPr>
      <w:r>
        <w:drawing>
          <wp:inline distT="0" distB="0" distL="0" distR="0">
            <wp:extent cx="{cx}" cy="{cy}"/>
            <wp:effectExtent l="0" t="0" r="0" b="0"/>
            <wp:docPr id="1" name="Captura_Blog_Alan_Castells" descr="Captura de pantalla del blog educativo de Alan Jareth Castells Montalvo"/>
            <wp:cNvGraphicFramePr>
              <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
            </wp:cNvGraphicFramePr>
            <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
              <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
                  <pic:nvPicPr>
                    <pic:cNvPr id="0" name="captura_blog.jpg"/>
                    <pic:cNvPicPr/>
                  </pic:nvPicPr>
                  <pic:blipFill>
                    <a:blip r:embed="{rel_id}"/>
                    <a:stretch>
                      <a:fillRect/>
                    </a:stretch>
                  </pic:blipFill>
                  <pic:spPr>
                    <a:xfrm>
                      <a:off x="0" y="0"/>
                      <a:ext cx="{cx}" cy="{cy}"/>
                    </a:xfrm>
                    <a:prstGeom prst="rect">
                      <a:avLst/>
                    </a:prstGeom>
                  </pic:spPr>
                </pic:pic>
              </a:graphicData>
            </a:graphic>
          </wp:inline>
        </w:drawing>
      </w:r>
    </w:p>"""

paragraphs = [
    # Encabezado / Portada
    make_p([("INSTITUTO CONSORCIO CLAVIJERO", True, False, "0F3D5E", 32, False)], align="center", space_before=120, space_after=80),
    make_p([("Módulo 3. Herramientas de Comunicación y Socialización Digital", True, False, "475569", 24, False)], align="center", space_after=240, border_bottom=True),
    
    # Datos de identificación requeridos en el Paso 3.1
    make_p([("DATOS DE IDENTIFICACIÓN DE LA ACTIVIDAD", True, False, "0F3D5E", 24, False)], space_before=120, space_after=120),
    make_p([("Título de la actividad: ", True, False, "1E293B", 22, False),
            ("Actividad 4. Herramientas de comunicación y socialización en mis estudios en línea (Elaboración de un blog educativo)", False, False, "1E293B", 22, False)], space_after=100),
    make_p([("Título del blog: ", True, False, "1E293B", 22, False),
            ("Conexión Digital ICC: Herramientas de Comunicación y Socialización en el Aprendizaje en Línea", False, True, "1E293B", 22, False)], space_after=100),
    make_p([("Nombre del alumno (Autor): ", True, False, "1E293B", 22, False),
            ("Alan Jareth Castells Montalvo", True, False, "0F3D5E", 22, False)], space_after=100),
    make_p([("Fecha de elaboración: ", True, False, "1E293B", 22, False),
            ("8 de noviembre de 2026", False, False, "1E293B", 22, False)], space_after=240, border_bottom=True),

    # Paso 3.1 Liga del blog
    make_p([("1. ENLACE (LINK) DE ACCESO PÚBLICO AL BLOG EDUCATIVO", True, False, "0F3D5E", 24, False)], space_before=160, space_after=100),
    make_p([("El blog ha sido configurado con acceso público sin restricciones para su revisión por parte del Docente Digital en la siguiente dirección electrónica:", False, False, "1E293B", 22, False)], align="both", space_after=120),
    make_p([("Enlace directo al blog: ", True, False, "0F3D5E", 22, False),
            ("https://alanhilo.github.io/blog-icc-actividad4/", True, False, "0284C7", 22, True)], space_after=240, shading="F0F9FF"),

    # Paso 3.1 Captura de pantalla incrustada
    make_p([("2. CAPTURA DE PANTALLA DE LA PUBLICACIÓN DEL BLOG", True, False, "0F3D5E", 24, False)], space_before=160, space_after=100),
    make_p([("A continuación, se presenta la evidencia visual (captura de pantalla) de la publicación realizada en el blog educativo:", False, False, "1E293B", 22, False)], align="both", space_after=100),
    make_image_p("rIdImg1", cx=5760000, cy=2610000),

    # Respaldo íntegro del contenido del post (para garantizar cumplimiento total de rúbrica)
    make_p([("3. CONTENIDO ÍNTEGRO PUBLICADO EN EL BLOG", True, False, "0F3D5E", 24, False)], space_before=200, space_after=120, border_bottom=True),
    make_p([("Título del Blog: ", True, False, "0F3D5E", 22, False),
            ("Conexión Digital ICC: Herramientas de Comunicación y Socialización en el Aprendizaje en Línea", True, False, "1E293B", 22, False)], space_after=80),
    make_p([("Autor(a): ", True, False, "0F3D5E", 22, False),
            ("Alan Jareth Castells Montalvo", True, False, "1E293B", 22, False)], space_after=140),
    make_p([("En la modalidad educativa en línea, la distancia física se transforma en cercanía intelectual gracias a la integración estratégica de las Tecnologías de la Información y la Comunicación (TIC). Para quienes cursamos nuestros estudios superiores en el Instituto Consorcio Clavijero (ICC), comprender las características y funciones de las herramientas de comunicación y socialización digital resulta indispensable para interactuar con el Docente Digital, colaborar con nuestros compañeros de aula virtual y gestionar nuestro aprendizaje de manera autónoma y organizada.", False, False, "1E293B", 22, False)], align="both", space_after=180),

    # Subtema 1: Herramientas de Comunicación
    make_p([("3.1. Herramientas de Comunicación Digital", True, False, "0284C7", 24, False)], space_before=120, space_after=100),
    
    make_p([("A) Correo electrónico", True, False, "0F3D5E", 22, False)], space_before=80, space_after=60),
    make_p([("Definición: ", True, False, "1E293B", 22, False),
            ("El correo electrónico (e-mail) es una herramienta de comunicación digital de carácter asíncrono que permite redactar, enviar, recibir y almacenar mensajes escritos, así como adjuntar archivos de diversa índole (documentos de texto, hojas de cálculo, presentaciones o imágenes) a través de la red de internet. Se distingue por contar con una estructura formal compuesta por destinatario, asunto, cuerpo del mensaje y firma, lo que lo convierte en el canal oficial por excelencia para la correspondencia institucional y académica.", False, False, "1E293B", 22, False)], align="both", space_after=80),
    make_p([("Ejemplo de aplicación en el ICC: ", True, False, "92400E", 22, False),
            ("Durante el trimestre en el Instituto Consorcio Clavijero, utilizo mi cuenta de correo institucional para enviar una consulta formal a mi Docente Digital solicitando orientación detallada sobre los criterios de la rúbrica de evaluación antes de la entrega dominical, adjuntando un avance preliminar de mi actividad. Asimismo, reviso diariamente mi bandeja de entrada para recibir los avisos oficiales sobre el calendario escolar, fechas de reinscripción y comunicados de coordinación académica.", False, False, "1E293B", 22, False)], align="both", space_after=140),

    make_p([("B) Mensajería instantánea", True, False, "0F3D5E", 22, False)], space_before=80, space_after=60),
    make_p([("Definición: ", True, False, "1E293B", 22, False),
            ("La mensajería instantánea es un servicio de comunicación primordialmente síncrono (en tiempo real) que facilita el intercambio inmediato de mensajes breves de texto, notas de voz, enlaces e imágenes entre dos personas o dentro de grupos de trabajo mediante dispositivos conectados a internet (como WhatsApp, Telegram, Google Chat o el mensajero interno de la plataforma educativa). Su principal característica es la inmediatez y fluidez en la respuesta para coordinar tareas operativas.", False, False, "1E293B", 22, False)], align="both", space_after=80),
    make_p([("Ejemplo de aplicación en el ICC: ", True, False, "92400E", 22, False),
            ("En mi formación dentro del ICC, empleo el mensajero instantáneo de la plataforma educativa y un grupo de estudio en Google Chat/WhatsApp con mis compañeros de asignatura para resolver dudas puntuales de manera rápida, acordar la distribución de subtemas en un proyecto colaborativo y enviarnos recordatorios oportunos horas antes de que cierre el plazo de entrega el domingo por la noche.", False, False, "1E293B", 22, False)], align="both", space_after=140),

    make_p([("C) Videollamadas", True, False, "0F3D5E", 22, False)], space_before=80, space_after=60),
    make_p([("Definición: ", True, False, "1E293B", 22, False),
            ("Las videollamadas o videoconferencias son herramientas de comunicación síncrona audiovisual que permiten establecer sesiones interactivas en tiempo real transmitiendo audio y video simultáneamente entre participantes ubicados en diferentes lugares geográficos (por ejemplo, Google Meet, Zoom o Microsoft Teams). Además del contacto cara a cara virtual, integran funciones colaborativas como compartir pantalla, pizarra digital, grabación de sesiones y chat integrado.", False, False, "1E293B", 22, False)], align="both", space_after=80),
    make_p([("Ejemplo de aplicación en el ICC: ", True, False, "92400E", 22, False),
            ("A lo largo de mis estudios en el Instituto Consorcio Clavijero, asisto a las sesiones síncronas por videollamada en Google Meet convocadas por mi Docente Digital, en las cuales compartimos pantalla para analizar ejemplos prácticos de citación en formato APA y despejar dudas en vivo mediante el micrófono. También organizo videollamadas breves con compañeros para ensayar exposiciones virtuales y revisar documentos compartidos en tiempo real.", False, False, "1E293B", 22, False)], align="both", space_after=180),

    # Subtema 2: Herramientas de Socialización
    make_p([("3.2. Herramientas de Socialización Digital", True, False, "0D9488", 24, False)], space_before=120, space_after=100),

    make_p([("A) Redes sociales", True, False, "0F3D5E", 22, False)], space_before=80, space_after=60),
    make_p([("Definición: ", True, False, "1E293B", 22, False),
            ("Las redes sociales digitales son plataformas estructuradas en comunidades de usuarios (individuos u organizaciones) unidos por intereses comunes, actividades académicas o vínculos profesionales (tales como Facebook, LinkedIn, X o YouTube). Estas herramientas permiten crear perfiles, difundir recursos multimedia, comentar publicaciones y generar redes de colaboración e interacción social sin barreras espaciales.", False, False, "1E293B", 22, False)], align="both", space_after=80),
    make_p([("Ejemplo de aplicación en el ICC: ", True, False, "92400E", 22, False),
            ("Durante mi trayectoria como estudiante del ICC, sigo las redes sociales oficiales del Instituto Consorcio Clavijero para mantenerme al tanto de conferencias magistrales, talleres extracurriculares, convocatorias de becas y eventos institucionales; además, participo en comunidades académicas y grupos de mi licenciatura para intercambiar infografías, recomendar bibliografía confiable y fortalecer el sentido de pertenencia con la comunidad estudiantil.", False, False, "1E293B", 22, False)], align="both", space_after=140),

    make_p([("B) Blogs", True, False, "0F3D5E", 22, False)], space_before=80, space_after=60),
    make_p([("Definición: ", True, False, "1E293B", 22, False),
            ("Un blog (o bitácora digital) es un sitio web actualizado periódicamente que recopila publicaciones —denominadas entradas o posts— ordenadas de forma cronológica inversa (de la más reciente a la más antigua), escritas por uno o varios autores sobre temáticas específicas. Los blogs educativos fomentan la organización estructurada mediante títulos y subtemas, el pensamiento crítico, la divulgación del conocimiento y la retroalimentación a través de una sección de comentarios (Nieves, 2025).", False, False, "1E293B", 22, False)], align="both", space_after=80),
    make_p([("Ejemplo de aplicación en el ICC: ", True, False, "92400E", 22, False),
            ("Como parte de las evidencias de aprendizaje en el ICC —tal como en esta Actividad 4—, elaboro y publico un blog con fines educativos utilizando mi cuenta institucional para redactar artículos propios, definir conceptos clave de mis materias, ejemplificar el uso de tecnologías y compartir mis reflexiones respaldadas con referencias en formato APA para que mi Docente Digital y compañeros puedan consultarlas públicamente.", False, False, "1E293B", 22, False)], align="both", space_after=140),

    make_p([("C) Páginas personales", True, False, "0F3D5E", 22, False)], space_before=80, space_after=60),
    make_p([("Definición: ", True, False, "1E293B", 22, False),
            ("Las páginas personales son sitios web diseñados y administrados por un individuo (creados en plataformas como Google Sites, WordPress o GitHub Pages) cuya estructura es principalmente estática y jerárquica, a diferencia del orden cronológico de un blog. Su función es presentar el perfil biográfico y académico del autor, centralizar un portafolio digital de evidencias, recopilar proyectos destacados y ofrecer datos de contacto profesional.", False, False, "1E293B", 22, False)], align="both", space_after=80),
    make_p([("Ejemplo de aplicación en el ICC: ", True, False, "92400E", 22, False),
            ("A lo largo de mis trimestres en el Instituto Consorcio Clavijero, diseño una página personal en Google Sites que funciona como mi portafolio digital universitario, donde organizo por pestañas mi semblanza académica, los mejores proyectos integradores, ensayos e investigaciones desarrollados en cada asignatura, consolidando así una carta de presentación profesional para mi futuro egreso laboral.", False, False, "1E293B", 22, False)], align="both", space_after=200),

    # Criterio 6: Referencias Bibliográficas APA (con los 4 elementos obligatorios: Autor, Fecha, Título y Fuente/Enlace)
    make_p([("4. REFERENCIAS BIBLIOGRÁFICAS (FORMATO APA 7.ª EDICIÓN)", True, False, "0F3D5E", 24, False)], space_before=200, space_after=140, border_bottom=True),

    make_p([("Instituto Consorcio Clavijero [ICC]. (2026). ", False, False, "1E293B", 22, False),
            ("Módulo 3. Herramientas de comunicación y socialización digital", False, True, "1E293B", 22, False),
            (" [Material de estudio del curso]. Plataforma Educativa del Instituto Consorcio Clavijero. ", False, False, "1E293B", 22, False),
            ("https://desarrollo.clavijero.edu.mx/cursos/pregrado/basicas/trimestre_1/MACCBA0225/modulo3/actividades/actividad4/index.html", False, False, "0284C7", 22, True)],
           align="left", space_after=140, hanging=720, left=720),

    make_p([("Nieves, G. D. (2025, 26 de junio). ", False, False, "1E293B", 22, False),
            ("Características de un blog y sus componentes esenciales", False, True, "1E293B", 22, False),
            (". PostedIn. ", False, False, "1E293B", 22, False),
            ("https://www.postedin.com/blog/caracteristicas-blog-componentes-esenciales/", False, False, "0284C7", 22, True)],
           align="left", space_after=140, hanging=720, left=720),

    make_p([("PrograMate. (2022, 3 de enero). ", False, False, "1E293B", 22, False),
            ("Cómo crear un blog en Blogger paso a paso [2026]", False, True, "1E293B", 22, False),
            (" [Video]. YouTube. ", False, False, "1E293B", 22, False),
            ("https://www.youtube.com/watch?v=39FD-FO9L5E", False, False, "0284C7", 22, True)],
           align="left", space_after=140, hanging=720, left=720),
]

body_xml = "".join(paragraphs)

document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
    {body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

base_dir = os.path.dirname(__file__)
output_path = os.path.join(base_dir, "A4_AlanCastells.docx")
image_path = os.path.join(base_dir, "captura_blog.jpg")

with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as docx:
    docx.writestr("[Content_Types].xml", content_types_xml)
    docx.writestr("_rels/.rels", rels_xml)
    docx.writestr("word/_rels/document.xml.rels", doc_rels_xml)
    docx.writestr("word/styles.xml", styles_xml)
    docx.writestr("word/document.xml", document_xml)
    docx.write(image_path, "word/media/captura_blog.jpg")

print("Archivo Word con captura incrustada creado exitosamente en:", output_path)
