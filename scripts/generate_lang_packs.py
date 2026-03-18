import os

# PolyContract Language Expansion Script
# Automatically generates modular localized .tex files for rendering engines
# Supported: ZH_CN, ZH_TW, JA, KO, DE, FR, ES, IT, RU, PT, NL

langs = {
    "zh_cn": "简体中文", "zh_tw": "繁體中文", "ja": "日本語", "ko": "한국어",
    "de": "Deutsch", "fr": "Français", "es": "Español", "it": "Italiano",
    "ru": "Русский", "pt": "Português", "nl": "Nederlands"
}

clauses = {
    "01_parties.tex": {
        "zh_cn": r"\section*{1. 合同当事人}\n\textbf{出租人（房东）}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{承租人（租客）}\n\ContractTenants{SUFFIX}\n共同居住于：\Propaddress",
        "zh_tw": r"\section*{1. 合約當事人}\n\textbf{出租人（房東）}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{承租人（租客）}\n\ContractTenants{SUFFIX}\n共同居住於：\Propaddress",
        "ja": r"\section*{1. 契約当事者}\n\textbf{賃貸人（家主）}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{賃借人（借主）}\n\ContractTenants{SUFFIX}\n両者の住所：\Propaddress",
        "ko": r"\section*{1. 계약 당사자}\n\textbf{임대인 (집주인)}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{임차인 (세입자)}\n\ContractTenants{SUFFIX}\n거주지: \Propaddress",
        "de": r"\section*{1. Vertragsparteien}\n\textbf{Vermieter}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{Mieter}\n\ContractTenants{SUFFIX}\nBeide wohnhaft in: \Propaddress",
        "fr": r"\section*{1. Parties Contractantes}\n\textbf{Propriétaire}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{Locataire}\n\ContractTenants{SUFFIX}\nRésidant à: \Propaddress",
        "es": r"\section*{1. Partes Contratantes}\n\textbf{Arrendador}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{Arrendatario}\n\ContractTenants{SUFFIX}\nResidiendo en: \Propaddress",
        "it": r"\section*{1. Parti Contraenti}\n\textbf{Locatore}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{Conduttore}\n\ContractTenants{SUFFIX}\nResidenza: \Propaddress",
        "ru": r"\section*{1. Стороны Договора}\n\textbf{Арендодатель}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{Арендатор}\n\ContractTenants{SUFFIX}\nАдрес: \Propaddress",
        "pt": r"\section*{1. Partes Contratantes}\n\textbf{Senhorio}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{Inquilino}\n\ContractTenants{SUFFIX}\nResidindo em: \Propaddress",
        "nl": r"\section*{1. Contractpartijen}\n\textbf{Verhuurder}\n\ContractLandlords{SUFFIX}\n\vspace{0.5cm}\n\textbf{Huurder}\n\ContractTenants{SUFFIX}\nBeiden wonend te: \Propaddress"
    },
    "02_subject.tex": {
        "zh_cn": r"\section*{2. 租赁标的}\n出租人声明其为\Propunitnumber 号公寓的唯一所有权人，户型为\Propdisposition，面积 \Propaream~m\textsuperscript{2}，位于 \Propfloor 层，建筑编号 \Propbuildingnumber，座落于 \Propcadastralterritory，地址：\Propaddress。\n\n房屋的详细设备以交接协议为准。承租人确认已对该房屋进行妥善检查。",
        "zh_tw": r"\section*{2. 租賃標的}\n出租人聲明其為\Propunitnumber 號公寓的唯一所有權人，戶型為\Propdisposition，面積 \Propaream~m\textsuperscript{2}，位於 \Propfloor 層，建築編號 \Propbuildingnumber，座落於 \Propcadastralterritory，地址：\Propaddress。\n\n房屋的詳細設備以交接協議為準。承租人確認已對該房屋進行妥善檢查。",
        "ja": r"\section*{2. 賃貸目的物}\n賃貸人は、\Propunitnumber 号室の唯一の所有者であることを宣言します。間取り \Propdisposition、面積 \Propaream~m\textsuperscript{2}、階数 \Propfloor、建物番号 \Propbuildingnumber、所在地 \Propcadastralterritory、住所 \Propaddress 。\n\n賃借人は当物件を検査し、使用に適した状態であることを確認します。",
        "ko": r"\section*{2. 임대 목적물}\n임대인은 \Propunitnumber 호의 유일한 소유자임을 선언합니다. 면적 \Propaream~m\textsuperscript{2}, \Propfloor 층, 주소 \Propaddress.\n\n임차인은 본 목적물을 확인하고 임대에 적합한 상태임을 확인합니다.",
        "de": r"\section*{2. Vertragsgegenstand}\nDer Vermieter erklärt, dass er der alleinige Eigentümer der Wohnung Nr. \Propunitnumber\ ist, mit der Aufteilung \Propdisposition, Fläche \Propaream~m\textsuperscript{2}, im \Propfloor\ Stock, Gebäude Nr. \Propbuildingnumber, unter der Adresse \Propaddress.\n\nDer Mieter bestätigt, die Wohnung besichtigt zu haben und diese in gutem Zustand ist.",
        "fr": r"\section*{2. Objet du Bail}\nLe Propriétaire déclare être l'unique propriétaire de l'appartement N° \Propunitnumber, agencement \Propdisposition, de \Propaream~m\textsuperscript{2}, situé à l'adresse \Propaddress.\n\nLe Locataire confirme avoir inspecté les lieux.",
        "es": r"\section*{2. Objeto del Arrendamiento}\nEl Arrendador declara ser el propietario exclusivo del apartamento \Propunitnumber, de \Propaream~m\textsuperscript{2}, ubicado en \Propaddress.\n\nEl Arrendatario confirma haber inspeccionado el apartamento.",
        "it": r"\section*{2. Oggetto del Contratto}\nIl Locatore dichiara di essere il proprietario esclusivo dell'appartamento n. \Propunitnumber, superficie \Propaream~m\textsuperscript{2}, situato in \Propaddress.",
        "ru": r"\section*{2. Предмет Договора}\nАрендодатель заявляет, что он является единственным собственником квартиры \Propunitnumber, площадь \Propaream~m\textsuperscript{2}, по адресу \Propaddress.",
        "pt": r"\section*{2. Objeto do Contrato}\nO Senhorio declara ser o proprietário exclusivo do apartamento nº \Propunitnumber, \Propaream~m\textsuperscript{2}, localizado em \Propaddress.",
        "nl": r"\section*{2. Object van de Huurovereenkomst}\nDe Verhuurder verklaart exclusief eigenaar te zijn van appartement nr. \Propunitnumber, \Propaream~m\textsuperscript{2}, adres \Propaddress."
    },
    "03_term.tex": {
        "zh_cn": r"\section*{3. 租赁期限}\n本合同定期自 \Rentstartdate 至 \Rentenddate 止。经双方书面同意，本合同可予以延长。若需终止，应提前三个月提出书面通知。",
        "zh_tw": r"\section*{3. 租賃期限}\n本合約定期自 \Rentstartdate 至 \Rentenddate 止。經雙方書面同意，本合約可予以延長。若需終止，應提前三個月提出書面通知。",
        "ja": r"\section*{3. 賃貸期間}\n本契約は \Rentstartdate から \Rentenddate までの定期とします。両当事者の書面による合意により延長可能です。解約の際は3ヶ月前までに書面で通知する必要があります。",
        "ko": r"\section*{3. 임대 기간}\n본 임대 기간은 \Rentstartdate 부터 \Rentenddate 까지입니다. 계약 연장은 서면 합의로 가능하며, 해지 시 3개월 전 서면 통지가 필요합니다.",
        "de": r"\section*{3. Mietdauer}\nDieser Vertrag ist befristet. Die Miete beginnt am \Rentstartdate\ und endet am \Rentenddate. Eine Vertragsverlängerung ist schriftlich möglich.",
        "fr": r"\section*{3. Durée du Bail}\nCe contrat est à durée déterminée. Le bail commence le \Rentstartdate\ et prend fin le \Rentenddate.",
        "es": r"\section*{3. Término del Contrato}\nEl contrato comienza el \Rentstartdate\ y termina el \Rentenddate. Puede extenderse mediante acuerdo escrito mutuo.",
        "it": r"\section*{3. Durata della Locazione}\nIl contratto ha inizio il \Rentstartdate\ e termina il \Rentenddate.",
        "ru": r"\section*{3. Срок Аренды}\nСрок действия договора: с \Rentstartdate\ по \Rentenddate. Возможно продление по письменному согласию.",
        "pt": r"\section*{3. Prazo do Contrato}\nO contrato tem início em \Rentstartdate\ e término em \Rentenddate.",
        "nl": r"\section*{3. Huurperiode}\nDe huur start op \Rentstartdate\ en eindigt op \Rentenddate."
    },
    "04_rent.tex": {
        "zh_cn": r"\section*{4. 租金与其他杂费}\n承租人承诺每月向出租人支付租金 \Rentrentamount,- CZK，及房屋服务月度预付款 \Rentservicesamount,- CZK。两项合计 \Renttotalamount,- CZK，必须在每月第 \Rentpaymentday 日前支付至银行账户：\Rentbankaccount。\n\n电信与网费将由承租人直接缴于运营商。",
        "zh_tw": r"\section*{4. 租金與其他雜費}\n承租人承諾每月向出租人支付租金 \Rentrentamount,- CZK，及房屋服務月度預付款 \Rentservicesamount,- CZK。兩項合計 \Renttotalamount,- CZK，必須在每月第 \Rentpaymentday 日前支付至銀行帳戶：\Rentbankaccount。\n\n電信與網費將由承租人直接繳於運營商。",
        "ja": r"\section*{4. 賃料およびその他の費用}\n賃借人は毎月 \Rentrentamount,- CZK の賃料と \Rentservicesamount,- CZK の共益費（合計 \Renttotalamount,- CZK）を、毎月 \Rentpaymentday 日までに指定の銀行口座（\Rentbankaccount）へ支払うものとします。",
        "ko": r"\section*{4. 임대료 및 비용}\n임차인은 월 임대료 \Rentrentamount,- CZK 및 관리비 \Rentservicesamount,- CZK (총액 \Renttotalamount,- CZK)을 매월 \Rentpaymentday 일까지 \Rentbankaccount 계좌로 지불해야 합니다.",
        "de": r"\section*{4. Miete und Nebenkosten}\nDer Mieter zahlt monatlich eine Miete von \Rentrentamount,- CZK sowie Nebenkostenvorauszahlungen von \Rentservicesamount,- CZK, was insgesamt \Renttotalamount,- CZK entspricht, jeweils fällig bis zum \Rentpaymentday. Tag des Monats auf das Konto: \Rentbankaccount.",
        "fr": r"\section*{4. Loyer et Charges}\nLe Locataire s'engage à payer un loyer de \Rentrentamount,- CZK et des charges de \Rentservicesamount,- CZK (total \Renttotalamount,- CZK) avant le \Rentpaymentday\ de chaque mois, sur le compte: \Rentbankaccount.",
        "es": r"\section*{4. Renta y Servicios}\nLa renta es de \Rentrentamount,- CZK y los servicios son \Rentservicesamount,- CZK (total \Renttotalamount,- CZK), pagaderos antes del día \Rentpaymentday\ al número de cuenta: \Rentbankaccount.",
        "it": r"\section*{4. Canone e Spese}\nIl canone è di \Rentrentamount,- CZK oltre a \Rentservicesamount,- CZK per le spese (totale \Renttotalamount,- CZK), pagabile entro il \Rentpaymentday\ del mese sul conto: \Rentbankaccount.",
        "ru": r"\section*{4. Арендная Плата и Услуги}\nАрендная плата составляет \Rentrentamount,- CZK, а услуги \Rentservicesamount,- CZK (итого \Renttotalamount,- CZK). Оплата до \Rentpaymentday\ числа на счет: \Rentbankaccount.",
        "pt": r"\section*{4. Renda e Despesas}\nA renda é de \Rentrentamount,- CZK e as despesas de \Rentservicesamount,- CZK (total \Renttotalamount,- CZK), a pagar até o dia \Rentpaymentday\ na conta: \Rentbankaccount.",
        "nl": r"\section*{4. Huur en Servicekosten}\nDe huur bedraagt \Rentrentamount,- CZK en servicekosten \Rentservicesamount,- CZK (totaal \Renttotalamount,- CZK), te betalen voor de \Rentpaymentday\e van de maand op rekening: \Rentbankaccount."
    },
    "05_deposit.tex": {
        "zh_cn": r"\section*{5. 租赁押金}\n在签订本合同后，承租人向出租人缴纳无息押金 \DepositAmount,- CZK。合同到期后如无未结清的欠款和赔偿，该押金应全额退还。如押金被抵扣，承租人有义务在 15 日内补齐。",
        "zh_tw": r"\section*{5. 租賃押金}\n在簽訂本合約後，承租人向出租人繳納無息押金 \DepositAmount,- CZK。合約到期後如無未結清的欠款和賠償，該押金應全額退還。如押金被抵扣，承租人有義務在 15 日內補齊。",
        "ja": r"\section*{5. 敷金（保証金）}\n当契約締結にあたり、賃借人は無利子の敷金として \DepositAmount,- CZK を支払います。契約終了時、債務を精算した上で返還されます。",
        "ko": r"\section*{5. 보증금}\n임차인은 무이자 보증금 \DepositAmount,- CZK 을 지불했습니다. 보증금은 임대 기간 종료 시 미납금 등이 없을 경우 전액 환불됩니다.",
        "de": r"\section*{5. Mietkaution}\nBei Vertragsunterzeichnung übergibt der Mieter dem Vermieter eine zinsfreie Kaution in Höhe von \DepositAmount,- CZK. Bei Zahlungsverzug kann der Vermieter diese verrechnen.",
        "fr": r"\section*{5. Dépôt de Garantie}\nÀ la signature, le Locataire transfère un dépôt sans intérêt de \DepositAmount,- CZK. Il sera rendu après la fin du bail à condition qu'aucune dette n'y soit associée.",
        "es": r"\section*{5. Depósito de Seguridad}\nEl Arrendatario otorga un depósito sin intereses de \DepositAmount,- CZK. Este será devuelto tras el término del contrato y la liquidación de las deudas.",
        "it": r"\section*{5. Deposito Cauzionale}\nIl Conduttore versa un deposito cauzionale di \DepositAmount,- CZK, che verrà restituito a fine locazione previa verifica di eventuali danni o insoluti.",
        "ru": r"\section*{5. Гарантийный Залог}\nАрендатор внес залог в размере \DepositAmount,- CZK. Залог возвращается после окончания договора при отсутствии задолженностей.",
        "pt": r"\section*{5. Caução}\nO Inquilino entregou uma caução no valor de \DepositAmount,- CZK, a ser devolvida no fim do contrato após liquidação de eventuais dívidas.",
        "nl": r"\section*{5. Borgsom}\nDe Huurder betaalt een borgsom van \DepositAmount,- CZK. Deze wordt aan het eind van de huurtermijn geretourneerd indien er geen verdere financiële vorderingen zijn."
    },
    "06_handover.tex": {
        "zh_cn": r"\section*{6. 房屋交接}\n出租人承诺在租赁首日连同全套钥匙将房屋移交给承租人，并出具含有水电燃气表读数的交房确认表（协议书）；期满退租时，承租人也应将房屋保持原有良好状态（含正常损耗）并交还房屋及结清注销户口。",
        "zh_tw": r"\section*{6. 房屋交接}\n出租人承諾在租賃首日連同全套鑰匙將房屋移交給承租人，並出具含有水電燃氣表讀數的交房確認表（協議書）；期滿退租時，承租人也應將房屋保持原有良好狀態（含正常損耗）並交還房屋及結清註銷戶口。",
        "ja": r"\section*{6. 物件の引き渡し}\n賃貸人は契約開始日に鍵とともに物件を引き渡します。その際、メーターの数値等を記載した引渡書を作成します。契約終了時には、賃借人は原状回復（通常損耗を除く）した上で物件を返還するものとします。",
        "ko": r"\section*{6. 주택 양도}\n임대인은 임대 시작일까지 열쇠를 포함한 목적물을 임차인에게 양도해야 합니다. 반환 시, 임차인은 일반적인 마모를 제외한 원래 상태로 주택을 반환해야 합니다.",
        "de": r"\section*{6. Wohnungsübergabe}\nDer Vermieter verpflichtet sich, dem Mieter die Wohnung bis spätestens Mietbeginn zu übergeben. Es wird ein Übergabeprotokoll inkl. der Zählerstände angefertigt.",
        "fr": r"\section*{6. Remise des Clefs}\nLe Propriétaire s'engage à remettre l'appartement au plus tard le jour du début du bail. Un état des lieux d'entrée et de sortie sera effectué.",
        "es": r"\section*{6. Entrega del Apartamento}\nEl Arrendador se compromete a entregar el piso mediante un acta de entrega inicial con las lecturas de los servicios.",
        "it": r"\section*{6. Consegna dell'Appartamento}\nIl Locatore consegnerà l'appartamento con relativo verbale di consegna comprendente anche le letture delle utenze domestiche.",
        "ru": r"\section*{6. Передача Квартиры}\nАрендодатель обязуется передать квартиру до даты начала аренды с подписанием акта приема-передачи.",
        "pt": r"\section*{6. Entrega da Propriedade}\nO Senhorio compromete-se a entregar o imóvel mediante auto de vistoria onde constam as leituras dos contadores.",
        "nl": r"\section*{6. Oplevering van het Appartement}\nDe Verhuurder draagt het appartement uiterlijk over op de aanvangsdag middels een opleveringsprotocol incl. meterstanden."
    },
    "07_rights.tex": {
        "zh_cn": r"\section*{7. 权利与义务}\n\textbf{出租人的义务：} 确保房屋适宜居住并自行负担重大维修费用。\n\textbf{出租人的权利：} 定期进行检查；当承租人未能履责时自行处理并要求承租人赔偿。\n\textbf{承租人的义务：} 仅将房屋作为居住使用；保持室内清洁与运转良善；承担 1000 CZK 以下的小额日常修理；不在室内吸烟，且不允许转租或作为商业用处。",
        "zh_tw": r"\section*{7. 權利與義務}\n\textbf{出租人的義務：} 確保房屋適宜居住並自行負擔重大維修費用。\n\textbf{出租人的權利：} 定期進行檢查；當承租人未能履責時自行處理並要求承租人賠償。\n\textbf{承租人的義務：} 僅將房屋作為居住使用；保持室內清潔與運轉良善；承擔 1000 CZK 以下的小額日常修理；不在室內吸菸，且不允許轉租或作為商業用處。",
        "ja": r"\section*{7. 権利および義務}\n\textbf{賃貸人の義務：} 居住に適した状態で物件を引き渡し、大規模な修繕費用を負担すること。\n\textbf{賃借人の義務：} もっぱら居住用として使用し、清潔に保つこと。また室内での喫煙や第三者への転貸（又貸し）を禁じます。",
        "ko": r"\section*{7. 권리 및 의무}\n\textbf{임대인의 의무:} 거주에 적합한 상태로 목적물을 유지하고 중대한 수리를 책임집니다.\n\textbf{임차인의 의무:} 주거용으로만 사용하고 깨끗하게 유지하며, 무단 전대 및 흡연을 금지합니다.",
        "de": r"\section*{7. Rechte und Pflichten}\n\textbf{Pflichten des Vermieters:} Übergabe der Wohnung im ordnungsgemäßen Zustand und Übernahme größerer Reparaturen.\n\textbf{Pflichten des Mieters:} Ausschließliche Nutzung zu Wohnzwecken, Übernahme von Kleinreparaturen, Verbot der Untervermietung und des Rauchens in der Wohnung.",
        "fr": r"\section*{7. Droits et Obligations}\n\textbf{Obligations du Locataire:} Maintenir le logement en bon état de propreté, payer les petites réparations régulières, interdiction formelle de sous-louer et de fumer.",
        "es": r"\section*{7. Derechos y Obligaciones}\n\textbf{Obligaciones del Arrendatario:} Mantener el piso limpio, asumir reparaciones menores inmediatas, y no subarrendar ni fumar.",
        "it": r"\section*{7. Diritti e Doveri}\n\textbf{Obblighi del Conduttore:} Usare l'appartamento solo per uso abitativo, tenerlo pulito, eseguire le piccole manutenzioni ordinarie e divieto di fumo/subaffitto.",
        "ru": r"\section*{7. Права и Обязанности}\n\textbf{Обязанности Арендатора:} Использовать только для проживания, поддерживать чистоту, производить мелкий ремонт; субаренда и курение запрещены.",
        "pt": r"\section*{7. Direitos e Obrigações}\n\textbf{Obrigações do Inquilino:} Utilizar o imóvel exclusivamente para habitação, realizar pequenas reparações, sendo proibido subarrendar e fumar.",
        "nl": r"\section*{7. Rechten en Plichten}\n\textbf{Plichten van de Huurder:} De woning enkel gebruiken voor woondoeleinden, kleine mankementen zelf repareren, en een rook- en onderhuurverbod in acht nemen."
    },
    "08_final.tex": {
        "zh_cn": r"\section*{8. 最终条款}\n\begin{enumerate}[label=\arabic*.]\n\item 双方权责等未尽事宜严格遵循民法典（第 89/2012 Coll. 号）法案执行。\n\item 任何补充或删改须采取书面附件形式并经双方共同签署生效。\n\item 本合同自双方签署后正式生效。双方确认此文件反映双方真实的自由意愿。\n\end{enumerate}\n\vspace{2cm}\n签订于 \ContractPlace，日期 \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm}出租人 \hfill 承租人 \\",
        "zh_tw": r"\section*{8. 最終條款}\n\begin{enumerate}[label=\arabic*.]\n\item 雙方權責等未盡事宜嚴格遵循民法典（第 89/2012 Coll. 號）法案執行。\n\item 任何補充或刪改須採取書面附件形式並經雙方共同簽署生效。\n\item 本合約自雙方簽署後正式生效。雙方確認此文件反映雙方真實的自由意願。\n\end{enumerate}\n\vspace{2cm}\n簽訂於 \ContractPlace，日期 \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm}出租人 \hfill 承租人 \\",
        "ja": r"\section*{8. 最終条項}\n\begin{enumerate}[label=\arabic*.]\n\item 本契約に定めのない事項は関連法規（民法典）に従います。\n\item 契約の変更は双方の書面合意のみ有効です。\n\end{enumerate}\n\vspace{2cm}\n作成地: \ContractPlace, 日付: \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm} 賃貸人 \hfill 賃借人 \\",
        "ko": r"\section*{8. 최종 조항}\n본 계약의 수정 및 보충은 양 당사자의 서면 동의로만 이루어집니다. 본 계약은 당사자들의 자유로운 의지에 의해 체결되었음을 확인합니다.\n\vspace{2cm}\n서명 장소: \ContractPlace \ \ 일자: \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm} 임대인 \hfill 임차인 \\",
        "de": r"\section*{8. Schlussbestimmungen}\n\begin{enumerate}[label=\arabic*.]\n\item Nicht geregelte Rechte richten sich nach dem tschechischen BGB (Gesetz Nr. 89/2012 Slg.).\n\item Änderungen bedürfen der Schriftform.\n\item Die Parteien erklären, dies bei freiem Willen unterzeichnet zu haben.\n\end{enumerate}\n\vspace{2cm}\nIn \ContractPlace \ am \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm} Vermieter \hfill Mieter \\",
        "fr": r"\section*{8. Dispositions Finales}\nCe contrat est soumis à la loi (Code Civil N° 89/2012 Coll.). Tous les ajouts doivent être faits par écrit. \n\vspace{2cm}\nFait à \ContractPlace \ le \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm} Propriétaire \hfill Locataire \\",
        "es": r"\section*{8. Disposiciones Finales}\nLas partes celebran este contrato según sus plenos derechos y bajo la ley civil (No. 89/2012). \n\vspace{2cm}\nEn \ContractPlace, \ a \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm} Arrendador \hfill Arrendatario \\",
        "it": r"\section*{8. Disposizioni Finali}\nEventuali modifiche a questo accordo dovranno essere redatte congiuntamente in forma scritta. \n\vspace{2cm}\nA \ContractPlace, \ il \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm} Locatore \hfill Conduttore \\",
        "ru": r"\section*{8. Заключительные Положения}\nНастоящий договор вступает в силу с момента его заключения. \n\vspace{2cm}\nВ \ContractPlace, \ \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm} Арендодатель \hfill Арендатор \\",
        "pt": r"\section*{8. Disposições Finais}\nEste contrato entra em vigor na data da sua assinatura. Quaisquer alterações devem ser efetuadas por escrito.\n\vspace{2cm}\nEm \ContractPlace, \ em \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm} Senhorio \hfill Inquilino \\",
        "nl": r"\section*{8. Slotbepalingen}\nDit huurcontract wordt beheerst door het geldende recht. Wijzigingen vereisen een schriftelijke vastlegging.\n\vspace{2cm}\nTe \ContractPlace, \ op \ContractDate \hfill \underline{\hspace{5cm}} \\ \vspace{1.5cm}\n\underline{\hspace{5cm}} \hfill \underline{\hspace{5cm}} \\ \vspace{0.2cm} Verhuurder \hfill Huurder \\"
    }
}

def generate_packs():
    base_dir = "src/modules"
    # Ensure modules dir exists
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Loop through each language to generate the directory and files
    for lang in langs.keys():
        lang_dir = os.path.join(base_dir, lang)
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)

        # Iterate over 8 clauses
        for filename, translations in clauses.items():
            content = translations.get(lang, "")
            
            # Since our strings have explicit "\n", we should ensure proper newline formatting in file
            # However `r"\section..."` handles raw strings. But to split by explicit raw `\n` we replace them.
            # actually we can just format them properly.
            content = content.replace('{SUFFIX}', lang.replace('_', '').upper())
            content = content.replace('\\n', '\n')

            filepath = os.path.join(lang_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content + "\n")
        print(f"Generated language pack: {lang.upper()} ({langs[lang]})")

if __name__ == "__main__":
    generate_packs()
