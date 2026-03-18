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

-- Setup iteration capability for landlords and tenants
-- Because latex arrays are hard, we'll build latex content dynamically here for the lists
local function generate_party_latex(list, role)
    local out = ""
    for i, person in ipairs(list) do
        out = out .. "\\textbf{" .. (person.name or "") .. "}\\\\"
        if person.birth_date then out = out .. "datum narození/DOB: " .. person.birth_date .. "\\\\" end
        if person.passport then out = out .. "č.pasu/Passport: " .. person.passport .. "\\\\" end
        if person.address then out = out .. "Adresa/Address: " .. person.address .. "\\\\" end
        if person.phone then out = out .. "Mobil/Phone: " .. person.phone .. "\\\\" end
        if person.email then out = out .. "Email: " .. person.email .. "\\\\" end
        
        if i < #list then
            out = out .. "\\vspace{0.2cm}\\textit{a / and}\\vspace{0.2cm}\\\\"
        end
    end
    tex_print("\\newcommand{\\Contract" .. role .. "s}{" .. out .. "}")
end

generate_party_latex(data.landlords, "Landlord")
generate_party_latex(data.tenants, "Tenant")

-- Expose language list and active modules to TeX
local langs = ""
for i, l in ipairs(data.project.languages) do
    langs = langs .. l .. ","
end
tex_print("\\newcommand{\\ActiveLangs}{" .. langs .. "}")

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

