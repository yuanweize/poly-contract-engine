local lfs = require("lfs")
local tex_print = tex and tex.print or print

-- Read data.json from the parent directory
local file = io.open("../data.json", "r")
if not file then
    tex_print("\\textbf{Error: ../data.json not found!}")
    return
end
local content = file:read("*a")
file:close()

-- A simple lightweight JSON parser 
local function parse_json(str)
    if not str then return nil end
    local function parse_value(s, pos)
        local value, next_pos
        -- skip whitespace
        pos = s:find("[^%s]", pos)
        if not pos then return nil, pos end
        local c = s:sub(pos, pos)
        
        if c == '"' then
            next_pos = s:find('"', pos + 1)
            value = s:sub(pos + 1, next_pos - 1)
            return value, next_pos + 1
        elseif c == '{' then
            value = {}
            pos = pos + 1
            while true do
                pos = s:find("[^%s]", pos)
                if s:sub(pos, pos) == '}' then return value, pos + 1 end
                if s:sub(pos, pos) == ',' then pos = pos + 1 end
                
                local key
                key, pos = parse_value(s, pos)
                
                pos = s:find(":", pos) + 1
                local item_val
                item_val, pos = parse_value(s, pos)
                
                value[key] = item_val
            end
        elseif c == '[' then
            value = {}
            pos = pos + 1
            local i = 1
            while true do
                pos = s:find("[^%s]", pos)
                if s:sub(pos, pos) == ']' then return value, pos + 1 end
                if s:sub(pos, pos) == ',' then pos = pos + 1 end
                
                local item_val
                item_val, pos = parse_value(s, pos)
                value[i] = item_val
                i = i + 1
            end
        end
        return nil, pos
    end
    local data, _ = parse_value(str, 1)
    return data
end

local data = parse_json(content)
if not data then
    tex_print("\\textbf{Error: Failed to parse JSON!}")
    return
end

-- Helper to safely define a LaTeX command
local function define_tex_cmd(cmd_name, value)
    if value == nil then value = "" end
    -- Escape some basic latex chars if necessary, but assume json data is safe-ish for now
    value = tostring(value):gsub("&", "\\&"):gsub("%%", "\\%%")
    tex_print("\\newcommand{\\" .. cmd_name .. "}{" .. value .. "}")
end

-- Generate Configuration Commands
define_tex_cmd("ContractDate", data.contract.date)
define_tex_cmd("ContractPlace", data.contract.place)

-- Generate Property Commands
for k, v in pairs(data.property) do
    -- Remove any character that is not a letter since LaTeX macros can only contain A-Za-z
    local clean_k = k:gsub("[^%a]", "")
    define_tex_cmd("Prop" .. clean_k, v)
end

-- Generate Rent Commands
for k, v in pairs(data.rent_details) do
    local clean_k = k:gsub("[^%a]", "")
    define_tex_cmd("Rent" .. clean_k, v)
end
define_tex_cmd("DepositAmount", data.deposit.amount)

local i18n = {
    cz = { title = "Nájemní smlouva", dob = "datum narození", passport = "č.pasu", address = "Adresa", phone = "Mobil", email = "Email", and_word = "a" },
    en = { title = "Rental Agreement", dob = "DOB", passport = "Passport", address = "Address", phone = "Phone", email = "Email", and_word = "and" },
    zh_cn = { title = "房屋租赁合同", dob = "出生日期", passport = "护照号", address = "地址", phone = "手机", email = "邮箱", and_word = "和" },
    zh_tw = { title = "房屋租賃合約", dob = "出生日期", passport = "護照號", address = "地址", phone = "手機", email = "郵箱", and_word = "和" },
    ja = { title = "賃貸借契約書", dob = "生年月日", passport = "パスポート番号", address = "住所", phone = "電話番号", email = "メール", and_word = "と" },
    ko = { title = "임대차 계약서", dob = "생년월일", passport = "여권 번호", address = "주소", phone = "전화번호", email = "이메일", and_word = "및" },
    de = { title = "Mietvertrag", dob = "Geburtsdatum", passport = "Reisepass Nr.", address = "Adresse", phone = "Telefon", email = "E-Mail", and_word = "und" },
    fr = { title = "Contrat de Location", dob = "Date de naissance", passport = "Passeport", address = "Adresse", phone = "Téléphone", email = "Email", and_word = "et" },
    es = { title = "Contrato de Arrendamiento", dob = "Fecha de nacimiento", passport = "Pasaporte", address = "Dirección", phone = "Teléfono", email = "Correo", and_word = "y" },
    it = { title = "Contratto di Locazione", dob = "Data di nascita", passport = "Passaporto", address = "Indirizzo", phone = "Telefono", email = "Email", and_word = "e" },
    ru = { title = "Договор Аренды", dob = "Дата рождения", passport = "Паспорт", address = "Адрес", phone = "Телефон", email = "Email", and_word = "и" },
    pt = { title = "Contrato de Arrendamento", dob = "Data de nascimento", passport = "Passaporte", address = "Endereço", phone = "Telefone", email = "Email", and_word = "e" },
    nl = { title = "Huurovereenkomst", dob = "Geboortedatum", passport = "Paspoort", address = "Adres", phone = "Telefoon", email = "E-mail", and_word = "en" }
}

for i, lang in ipairs(data.project.languages) do
    local trans = i18n[lang] or i18n["en"]
    local lang_suffix = lang:gsub("_", ""):upper()
    
    tex_print("\\newcommand{\\ContractTitle" .. lang_suffix .. "}{" .. trans.title .. "}")
    
    local function generate_party_latex(list, role)
        local out = ""
        for idx, person in ipairs(list) do
            out = out .. "\\textbf{" .. (person.name or "") .. "}\\\\"
            if person.birth_date then out = out .. trans.dob .. ": " .. person.birth_date .. "\\\\" end
            if person.passport then out = out .. trans.passport .. ": " .. person.passport .. "\\\\" end
            if person.address then out = out .. trans.address .. ": " .. person.address .. "\\\\" end
            if person.phone then out = out .. trans.phone .. ": " .. person.phone .. "\\\\" end
            if person.email then out = out .. trans.email .. ": " .. person.email .. "\\\\" end
            
            if idx < #list then
                out = out .. "\\vspace{0.2cm}\\textit{" .. trans.and_word .. "}\\vspace{0.2cm}\\\\"
            end
        end
        tex_print("\\newcommand{\\Contract" .. role .. "s" .. lang_suffix .. "}{" .. out .. "}")
    end
    
    generate_party_latex(data.landlords, "Landlord")
    generate_party_latex(data.tenants, "Tenant")
end

-- Export Global Titles based on active selection
local lang1_suffix = data.project.languages[1]:gsub("_", ""):upper()
tex_print("\\newcommand{\\DocTitlePrimary}{\\ContractTitle" .. lang1_suffix .. "}")
if #data.project.languages > 1 then
    local lang2_suffix = data.project.languages[2]:gsub("_", ""):upper()
    tex_print("\\newcommand{\\DocTitleSecondary}{\\ContractTitle" .. lang2_suffix .. "}")
else
    tex_print("\\newcommand{\\DocTitleSecondary}{}")
end

-- Inject Dynamic Fonts and Languages
local polyglossia_map = {
    cz = "czech", en = "english", de = "german", fr = "french",
    es = "spanish", it = "italian", ru = "russian", pt = "portuguese", nl = "dutch"
}

local has_cjk = false
local cjk_locale = nil
local eur_langs = {}

for _, lang in ipairs(data.project.languages) do
    if lang == "zh_cn" or lang == "zh_tw" then
        has_cjk = true
        cjk_locale = "zh"
    elseif lang == "ja" then
        has_cjk = true
        cjk_locale = "ja"
    elseif lang == "ko" then
        has_cjk = true
        cjk_locale = "ko"
    elseif polyglossia_map[lang] then
        table.insert(eur_langs, polyglossia_map[lang])
    end
end

tex_print("\\usepackage{polyglossia}")
if #eur_langs > 0 then
    tex_print("\\setmainlanguage{" .. eur_langs[1] .. "}")
    if #eur_langs > 1 then
        tex_print("\\setotherlanguage{" .. eur_langs[2] .. "}")
    end
else
    tex_print("\\setmainlanguage{english}")
end

if has_cjk then
    tex_print("\\usepackage[default]{luatexja-fontspec}")
    if cjk_locale == "zh" then
        -- Force LuaTeX to use Fandol, standard Chinese font in TeXLive
        tex_print("\\setmainjfont{FandolSong-Regular.otf}[BoldFont=FandolHei-Regular.otf]")
    end
end

-- Generate the RenderModule macro based on active languages
tex_print("\\newcommand{\\RenderModule}[1]{")
if #data.project.languages == 2 then
    tex_print("\\begin{paracol}{2}")
    tex_print("\\switchcolumn[0]* \\input{modules/" .. data.project.languages[1] .. "/#1}")
    tex_print("\\switchcolumn[1] \\input{modules/" .. data.project.languages[2] .. "/#1}")
    tex_print("\\end{paracol}")
    tex_print("\\vspace{0.5cm}")
else
    tex_print("\\input{modules/" .. data.project.languages[1] .. "/#1}")
    tex_print("\\vspace{0.5cm}")
end
tex_print("}")

-- Print a latex command that loads the active modules
tex_print("\\newcommand{\\LoadModules}{")
for _, mod in ipairs(data.project.modules) do
    tex_print("\\RenderModule{" .. mod .. "}")
end
tex_print("}")

