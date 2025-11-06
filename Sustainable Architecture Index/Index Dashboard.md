## 📊 Sustainable Architecture Index – Dashboard

### 📍 Index Overview

```dataview
table
  file.link as "Entry",
  era,
  bioregion,
  crisis_context,
  historical_precedent,
  tags
from ""
where contains(tags, "sustainable-architecture-index")
sort era asc
```

---

### ✳️ Optional Thematic Filters

#### ✅ Post-Collapse Cluster

```dataview
table file.link, era, bioregion, crisis_context
from ""
where contains(tags, "post-collapse")
```

#### ✅ Healing Design Entries

```dataview
table file.link, bioregion, historical_precedent
from ""
where contains(tags, "healing-design")
```

#### ✅ Modular Housing Entries

```dataview
table file.link, era, crisis_context
from ""
where contains(tags, "modular-housing")
```

---

### 🔍 Tips

- Use this dashboard to explore and maintain your index.
- Add more filtered views using tag logic.
- This updates automatically as entries evolve.
