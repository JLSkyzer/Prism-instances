import zipfile, uuid, json, re
from pathlib import Path

mods_dir = Path('Survie/minecraft/mods')
chapters_dir = Path('Survie/minecraft/config/ftbquests/quests/chapters')

# Remove existing generated chapters
for path in chapters_dir.glob('mods_*_gen.snbt'):
    path.unlink()

# categorization keywords
categories = {
    'tech': {
        'title': 'Technologie',
        'icon': 'minecraft:redstone',
        'keywords': ['tech', 'mekanism', 'thermal', 'engineer', 'industrial', 'power', 'factory', 'automation', 'machine', 'energy', 'industrial', 'electric']
    },
    'magic': {
        'title': 'Magie',
        'icon': 'minecraft:enchanted_book',
        'keywords': ['magic', 'magie', 'spell', 'arcane', 'wizard', 'botania', 'ars', 'mana', 'apotheosis', 'mystic', 'sorcer', 'enchanted']
    },
    'agri': {
        'title': 'Agriculture',
        'icon': 'minecraft:wheat',
        'keywords': ['farm', 'crop', 'agri', 'plant', 'harvest', 'food', 'culinary', 'cuisine']
    },
    'explore': {
        'title': 'Exploration',
        'icon': 'minecraft:compass',
        'keywords': ['explor', 'biome', 'dungeon', 'quest', 'adventure', 'aether', 'earth', 'minecolon', 'twilight', 'end', 'nether']
    },
    'other': {
        'title': 'Divers',
        'icon': 'minecraft:chest',
        'keywords': []
    }
}

# helper to classify mod by jar name

def classify(name: str):
    lname = name.lower()
    for key, data in categories.items():
        for kw in data['keywords']:
            if kw in lname:
                return key
    return 'other'


def clean_name(name: str) -> str:
    """Return a user friendly mod name."""
    name = re.sub(r'[-_](?:mc)?\d.*', '', name)
    name = re.sub(r'[-_]+', ' ', name)
    return name.strip().title()

# Build mods data
mods_by_category = {key: [] for key in categories}

for jar in mods_dir.glob('*.jar'):
    try:
        with zipfile.ZipFile(jar) as z:
            names = z.namelist()
            modids = {n.split('/')[1] for n in names if n.startswith('assets/')}
            modids.discard('minecraft'); modids.discard('');
            if not modids:
                continue
            modid = sorted(modids)[0]
            items = [Path(n).stem for n in names if n.startswith(f'assets/{modid}/models/item/') and n.endswith('.json')]
            if not items:
                continue
            items = sorted(set(items))[:3]
            modname = jar.stem
            cat = classify(modname)
            mods_by_category[cat].append({
                'modid': modid,
                'modname': modname,
                'clean_name': clean_name(modname),
                'items': items
            })
    except zipfile.BadZipFile:
        pass

# Generate chapters
for order, (cat_key, data) in enumerate(categories.items(), start=1):
    mods = mods_by_category[cat_key]
    if not mods:
        continue
    chapter = {
        'id': uuid.uuid4().hex.upper(),
        'group': '',
        'order_index': order,
        'filename': f'mods_{cat_key}_gen',
        'title': data['title'],
        'icon': {'id': data['icon'], 'Count': '1b'},
        'default_quest_shape': '',
        'default_hide_dependency_lines': False,
        'quests': []
    }
    cols = 6
    spacing_x = 5
    spacing_y = 8
    prev_chain_last = None
    for idx, mod in enumerate(sorted(mods, key=lambda m: m['clean_name'])):
        col = idx % cols
        row = idx // cols
        x_base = col * spacing_x
        y_base = row * spacing_y
        prev_id = None
        for qn, item in enumerate(mod['items'], start=1):
            q_id = uuid.uuid4().hex.upper()
            t_id = uuid.uuid4().hex.upper()
            r_id = uuid.uuid4().hex.upper()
            titles = ['Découverte', 'Progression', 'Maîtrise']
            quest = {
                'x': float(x_base),
                'y': float(y_base + (qn-1)*2),
                'id': q_id,
                'title': f"{titles[qn-1]} : {mod['clean_name']}",
                'icon': {'id': f"{mod['modid']}:{item}", 'Count': '1b'},
                'tasks': [{
                    'id': t_id,
                    'type': 'item',
                    'item': {'id': f"{mod['modid']}:{item}", 'Count': '1b'}
                }],
                'rewards': [{
                    'id': r_id,
                    'type': 'xp',
                    'xp': 100 * qn
                }]
            }
            if prev_id:
                quest['dependencies'] = [prev_id]
            elif prev_chain_last:
                quest['dependencies'] = [prev_chain_last]
            chapter['quests'].append(quest)
            prev_id = q_id
        prev_chain_last = prev_id
    # write SNBT
    def to_snbt(obj, indent=0):
        sp = '        '
        if isinstance(obj, dict):
            if not obj:
                return '{ }'
            lines = ['{']
            for k, v in obj.items():
                lines.append(f"{sp*(indent+1)}{k}: {to_snbt(v, indent+1)}")
            lines.append(f"{sp*indent}}}")
            return '\n'.join(lines)
        elif isinstance(obj, list):
            if not obj:
                return '[]'
            lines = ['[']
            for i, v in enumerate(obj):
                comma = ',' if i < len(obj)-1 else ''
                lines.append(f"{sp*(indent+1)}{to_snbt(v, indent+1)}{comma}")
            lines.append(f"{sp*indent}]")
            return '\n'.join(lines)
        elif isinstance(obj, bool):
            return 'true' if obj else 'false'
        elif isinstance(obj, float):
            return f"{obj:.1f}d"
        elif isinstance(obj, int):
            return str(obj)
        elif isinstance(obj, str) and obj.endswith('b') and obj[:-1].isdigit():
            return obj
        else:
            return json.dumps(obj)

    snbt = '{\n' + '\n'.join(f"        {k}: {to_snbt(v,1)}" for k,v in chapter.items()) + '\n}\n'
    out_path = chapters_dir / f"mods_{cat_key}_gen.snbt"
    out_path.write_text(snbt, encoding='utf-8')
