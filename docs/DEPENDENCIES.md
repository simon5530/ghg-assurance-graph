# Phase 1 dependencies and licensing

Verified installed metadata 2026-09-26; exact artifacts/hashes in uv.lock.

| Runtime package | Version | License metadata |
|---|---|---|
| Pydantic | 2.13.5 | MIT |
| pydantic-core | 2.46.5 | MIT |
| Pint | 0.26.1 | BSD metadata; bundled license inspected, 3 clauses |
| RDFLib | 7.6.0 | BSD-3-Clause |
| annotated-types | 0.8.0 | MIT |
| typing-inspection | 0.4.4 | MIT |
| typing-extensions | 4.16.0 | PSF-2.0 |
| flexcache | 0.3 | BSD metadata; bundled license inspected, 3 clauses |
| flexparser | 0.4 | BSD-3-Clause |
| platformdirs | 4.11.15 | MIT |
| pyparsing | 3.3.3 | MIT |

Dependencies are installed through upstream distributions, not vendored or relicensed.
Retain upstream notices when redistributing. Original source/docs/synthetic fixtures
are MIT. No copied competitor code, licensed factor database, standard text, fonts
or images. Reference links do not transfer third-party rights. AGPL/custom/CC-BY
considerations for future reuse are explicit in [reference brief](REFERENCE_BRIEF.md).

Development tools (pytest, jsonschema, Ruff, pip-audit) are separately locked, not
runtime requirements. Build uses hatchling 1.27.0; CI installs uv 0.12.19. Python is
3.12.14. Runtime and complete development requirements exported separately from the lockfile
and audited with pip-audit 2.10.1: no known vulnerabilities found on 2026-09-26. This is a database snapshot,
not a security guarantee. No paid or cloud execution dependency.

## 0.2.0a1 additions — 2026-09-28
Installed distribution metadata and locked artifacts reviewed. pySHACL 0.31.0 and
RO-Crate 0.15.1 are Apache-2.0; owlrl 7.6.2 W3C-20150513; html5rdf 1.2.1 MIT;
prettytable 3.18.0 BSD-3-Clause; wcwidth 0.9.1 MIT; arcp 0.2.1 Apache-2.0;
click 8.5.0 BSD-3-Clause; Jinja2 3.1.6 BSD; MarkupSafe 3.0.3 BSD-3-Clause;
python-dateutil 2.9.0.post0 dual Apache/BSD; requests 2.34.2 Apache-2.0;
certifi 2026.7.22 MPL-2.0; charset-normalizer 3.5.1 MIT; idna 3.20 BSD-3-Clause;
urllib3 2.8.0 MIT; packaging 26.3 Apache-2.0 OR BSD-2-Clause; six 1.17.0 MIT.
All exact transitive versions/hashes remain in uv.lock. Dependencies are not vendored;
redistributors must retain upstream notices, including MPL obligations where relevant.
Core operations do not invoke these libraries' network capabilities.
