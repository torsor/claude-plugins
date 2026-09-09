--[[
  tex2torsor filter — generic Pandoc Lua filter for LaTeX→HTML conversion.

  Reads configuration from the 'tex2torsor' metadata key (set via --metadata-file).

  Pandoc's LaTeX reader converts unknown mdframed environments to Div elements
  whose class list contains the environment name, so the primary job here is
  remapping those class names to the CSS classes we actually want.

  Also handles:
    - RawBlock "latex" as a fallback for any environments Pandoc left raw
    - RawInline "latex" for any macros Pandoc didn't expand
    - CodeBlock: adds "shell" class if no language class is present
]]

local cfg_envs   = {}   -- env_name → { classes, label }
local cfg_macros = {}   -- macro_name → { html_tag, classes }

local function to_string_list(lst)
  local result = {}
  if lst then
    for _, v in ipairs(lst) do
      table.insert(result, pandoc.utils.stringify(v))
    end
  end
  return result
end

function Meta(meta)
  local t2t = meta["tex2torsor"]
  if not t2t then return end

  if t2t.environments then
    for name, spec in pairs(t2t.environments) do
      cfg_envs[name] = {
        classes = to_string_list(spec.classes),
        label   = spec.label and pandoc.utils.stringify(spec.label) or nil,
      }
    end
  end

  if t2t.macros then
    for name, spec in pairs(t2t.macros) do
      cfg_macros[name] = {
        html_tag = spec.html_tag and pandoc.utils.stringify(spec.html_tag) or "code",
        classes  = to_string_list(spec.classes),
      }
    end
  end
end

-- Primary path: Pandoc converts mdframed/custom environments to Div with env name as class.
function Div(el)
  for env_name, spec in pairs(cfg_envs) do
    if el.classes:includes(env_name) then
      local new_classes = pandoc.List(spec.classes or {})
      el.attr = pandoc.Attr(el.identifier, new_classes, el.attributes)

      if spec.label then
        local label_block = pandoc.Para({
          pandoc.Strong({ pandoc.Str(spec.label) }),
        })
        el.content:insert(1, label_block)
      end

      return el
    end
  end
end

-- Fallback: some environments may be left as raw LaTeX blocks.
function RawBlock(el)
  if el.format ~= "latex" then return nil end

  for env_name, spec in pairs(cfg_envs) do
    local begin_tag = "\\begin{" .. env_name .. "}"
    local end_tag   = "\\end{"   .. env_name .. "}"

    local s = el.text:find(begin_tag, 1, true)
    if s then
      local e = el.text:find(end_tag, s, true)
      if e then
        local inner = el.text:sub(s + #begin_tag, e - 1)
        local parsed = pandoc.read(inner, "latex")
        local blocks = parsed.blocks

        if spec.label then
          table.insert(blocks, 1, pandoc.Para({
            pandoc.Strong({ pandoc.Str(spec.label) }),
          }))
        end

        return pandoc.Div(blocks, pandoc.Attr("", spec.classes or {}))
      end
    end
  end
end

-- Fallback: macros Pandoc didn't expand (e.g. no \newcommand in the file).
function RawInline(el)
  if el.format ~= "latex" then return nil end

  for macro_name, spec in pairs(cfg_macros) do
    local pattern = "^\\" .. macro_name .. "{(.+)}$"
    local content = el.text:match(pattern)
    if content then
      local attr = pandoc.Attr("", spec.classes or {})
      if spec.html_tag == "code" then
        return pandoc.Code(content, attr)
      elseif spec.html_tag == "span" then
        return pandoc.Span({ pandoc.Str(content) }, attr)
      end
    end
  end
end

-- Add "shell" class to unlabeled code blocks for CSS targeting.
function CodeBlock(el)
  if #el.classes == 0 then
    el.classes:insert("shell")
    return el
  end
end

return {
  { Meta      = Meta },
  { Div       = Div, RawBlock = RawBlock, RawInline = RawInline, CodeBlock = CodeBlock },
}
