-- Pandoc Lua filter for the AKTU revision notebook.
-- Renders ```dot code blocks (Graphviz) into inline SVG figures with a
-- consistent black-and-white textbook style. Optional attributes:
--   engine=neato|dot|circo|fdp   (default: dot)
--   caption="Figure caption"
--   width=60%                     (CSS max width of the figure)

local DEFAULTS = [[
  graph [fontname="TeX Gyre Termes", fontsize=13, bgcolor="transparent", pad="0.15", nodesep="0.35", ranksep="0.45"];
  node  [fontname="TeX Gyre Termes", fontsize=13, shape=box, style="rounded", color="black", penwidth=1.1, margin="0.12,0.06"];
  edge  [fontname="TeX Gyre Termes", fontsize=12, color="black", penwidth=1.0, arrowsize=0.75];
]]

local function inject_defaults(src)
  -- insert defaults right after the first opening brace of the graph
  local s, e = src:find("{", 1, true)
  if not s then return src end
  return src:sub(1, e) .. "\n" .. DEFAULTS .. src:sub(e + 1)
end

function CodeBlock(el)
  if not el.classes:includes("dot") then return nil end
  local engine = el.attributes["engine"] or "dot"
  local ok, svg = pcall(pandoc.pipe, engine, {"-Tsvg"}, inject_defaults(el.text))
  if not ok then
    io.stderr:write("Graphviz error in block:\n" .. el.text .. "\n")
    return nil
  end
  svg = svg:gsub("<%?xml.-%?>", ""):gsub("<!DOCTYPE.->", ""):gsub("<!%-%-.-%-%->", "")
  local width = el.attributes["width"]
  local style = width and (' style="max-width:' .. width .. '"') or ""
  local html = '<figure class="fig"><div class="svgwrap"' .. style .. '>' .. svg .. '</div>'
  local cap = el.attributes["caption"]
  if cap then html = html .. '<figcaption>' .. cap .. '</figcaption>' end
  html = html .. '</figure>'
  return pandoc.RawBlock("html", html)
end
