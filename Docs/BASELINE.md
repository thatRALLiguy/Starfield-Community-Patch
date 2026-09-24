# Recovered SFCP 1.0.0 baseline

This fork starts from the user-supplied September 2024 SFCP 1.0.0 release. It has **not** yet been updated for Starfield 1.16.244 or consolidated with other patch projects.

The upstream `spriggit/` directory was still the June 17, 2024 export even though its changelog described 1.0.0. The restored directory now represents an export of the actual release, including the Grendel, Kodama, Shotty, and Maelstrom records missing from the older source. Original contributor credits and the repository's MIT license remain intact. No USFP or DLC-patch records have been incorporated.

## Authoritative reference and editable source

- `baseline/1.0.0/`: exact ESM and BA2 extracted from the supplied SFCP ZIP. These are the authoritative released bytes.
- `baseline/manifest.json`: archive provenance, file hashes, tool versions, validation status, and a hash lock for the restored plugin source and existing scripts/meshes.
- `spriggit/`: recovered YAML using translation package **0.36.13**, invoked through Spriggit CLI **0.41.0**. This export is useful for inspection and further development, but its rebuild is not yet approved for gameplay use.
- `Scripts/Source/`, `meshes/`, and `.xTranslator/`: retained upstream assets. Script source has not been proven equivalent to the compiled scripts inside the released BA2. Existing translation dictionaries remain available; the supplied release ESM itself is not localized, so this YAML export does not establish a multilingual release.

## Why source publication is gated

Both tested Spriggit versions passed their record-count/ID checks. A separate decompressed-record comparison caught differences those checks miss:

| Translation package | Records preserved | Exact records including payload and group membership | Findings |
|---|---:|---:|---|
| 0.41.0 | 834 / 834 | 602 | Loot-list entry loss and weapon-template changes; rejected |
| 0.36.13 | 834 / 834 | 666 | All 29 weapons exactly preserved; remaining differences need review |

For 0.36.13, 7 of the 168 differing records contain only reordered subrecords. Other changes include condition padding, ownership bytes, perk ATAV data, quest ANAM values, the TES4 header, and a worldspace XCLW value. Some may be harmless normalization, but they have not all been established as harmless. See `audit/05-spriggit-roundtrip.json` for the complete comparison. No record headers or group memberships differed under the comparison's rules; compression and version-control metadata are excluded.

Do not ship the raw Spriggit output or silently accept these differences. The baseline workflow packages only the hash-verified original release, and fails when source files change. It does not compile the unverified YAML into a public release.

## Verify or reproduce the reference package

Requires Python 3.11 or newer; no game installation is needed:

```powershell
python tools/verify_baseline.py
python tools/verify_baseline.py --package dist/SFCP-1.0.0-reference.zip
```

The ZIP's contents are byte-identical to the original two files; ZIP container metadata differs. This package is the historical SFCP 1.0.0 reference, not a newly tested current-game patch. The GitHub workflow verifies and uploads this reference as a workflow artifact only. The inherited automatic publishing pipelines have been replaced to avoid distributing an unverified conversion.

## Reproduce the conversion investigation

Download [Spriggit CLI 0.41.0](https://github.com/Mutagen-Modding/Spriggit/releases/tag/0.41.0). The root `.spriggit` pins translation package 0.36.13 and declares the two master styles, so a game Data folder is unnecessary for rebuilding this snapshot. Spriggit needs network access to install its translation package the first time. Use a NuGet configuration permitting the official nuget.org feed if your environment restricts package sources.

From the repository root, with output in an ignored working directory:

```powershell
Spriggit.CLI.exe serialize --InputPath baseline/1.0.0/StarfieldCommunityPatch.esm --OutputPath .tools/re-export --GameRelease Starfield --PackageName Spriggit.Yaml --PackageVersion 0.36.13 --Check true
Spriggit.CLI.exe deserialize --InputPath spriggit --OutputPath .tools/rebuilt/StarfieldCommunityPatch.esm
python audit/compare_plugin_payloads.py baseline/1.0.0/StarfieldCommunityPatch.esm .tools/rebuilt/StarfieldCommunityPatch.esm .tools/roundtrip.json
```

The comparator reports differences; it does not approve them. The master styles were checked against the installed masters' flags (Starfield.esm: 0x81; SFBGS003.esm: 0x481), and the no-Data-folder rebuild was tested.

Generated YAML retains whitespace inside game text and embedded activity JSON. Do not run automatic whitespace cleanup over these fields as part of baseline recovery. Handwritten files pass `git diff --check`; the raw generated export contains existing trailing spaces and embedded tabs.

## Next development milestone

Resolve the remaining conversion differences or adopt a validated editing/build path before shipping source changes. Then compare small groups of released SFCP fixes against current vanilla, and consolidate independently implemented or appropriately licensed community fixes. Public downloads do not by themselves establish permission to reuse another project's implementation. Keep provenance and contributor credit for every imported fix.

Do not regenerate the frozen-baseline hash lock just to make changed source pass. Replace this baseline-only gate with reviewed build-preservation checks when source development resumes.
