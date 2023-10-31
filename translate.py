from deep_translator import GoogleTranslator
from lxml import etree as ET

def translateText(text):
    translated = GoogleTranslator(source='auto', target='ru').translate(text)
    return translated

# Устанавливаем правильное пространство имен
# ET.register_namespace('','http://www.woltlab.com')

# Открываем документ
tree = ET.parse('com.woltlab.wcf_en.xml')
# tree = ET.parse('com.woltlab.wcf_ru copy.xml')
# tree = ET.parse('com.woltlab.wcf_ru.xml')
root = tree.getroot()

counter = 0;
total = 0
toolongstr = ""

for elem in root.iter():
    total += 1

for elem in root.iter():
    # Если строка содржит данные языковом пакете - меняем их
    if ("language" in elem.tag):
        elem.attrib["languagecode"] = "ru"
        elem.attrib["languagename"] = "Русский"
        elem.attrib["countrycode"] = "ru"
        
    # Если строка содржит фразы - переводим
    if ("item" in elem.tag):
        counter += 1
        
        print(f"{round(counter/5033*100)}% - {counter}/{total}", end="\r")

        if (("->" in elem.text or "$" in elem.text or "%" in elem.text or "|" in elem.text or "{" in elem.text)):
            elem.getparent().remove(elem)
            continue

        if (elem.text != None):
            if (len(elem.text) < 5000):
                text_tr = translateText(elem.text)
                if (text_tr != None):
                    elem.text = text_tr
            else:
                toolongstr += elem.attrib['name']+"\r"
            elem.text = ET.CDATA(elem.text)

tree.write('com.woltlab.wcf_ru.xml', encoding='utf-8')

print (f"Следующие фразы блыли слишком длинными для перевода:")
print (toolongstr)