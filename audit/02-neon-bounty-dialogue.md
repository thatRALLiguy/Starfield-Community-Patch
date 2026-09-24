# Small audit: Neon checkpoint bounty dialogue

Checked 2026-09-23. Scope: checkpoint quest 0032C7C0 and its four dialogue responses only. Fork source baseline: 0ad97d3eb087dafb91afbc4bbb1588598212cc87.

## Finding

The Community Patch fork already contains a condition-based fix for the reported stale-bounty warning. Its four response records use GetCrimeGold on the player for four faction references, rather than the stale CrimeBountyAmount global described in issue 319.

| Response FormID | Intended branch | Observed source conditions |
|---|---|---|
| 0032C7CA | No bounty, weapon drawn | Four GetCrimeGold equality checks; IsWeaponOut = 2 |
| 0032C7CB | Bounty, weapon drawn | Four GetCrimeGold > 0 checks joined by OR; IsWeaponOut = 2 |
| 0032C7CC | Bounty, weapon not drawn | Four GetCrimeGold > 0 checks joined by OR; IsWeaponOut < 2 |
| 0032C7CD | No bounty, weapon not drawn | Four GetCrimeGold equality checks; IsWeaponOut < 2 |

Each runs bounty checks on player reference 000014:Starfield.esm, with faction parameters 05BD93, 0638E5, 26FDEA, and 26310C. Zero comparison values are omitted in the YAML. None of these four conditions references global 009108.

Issue 319 has a maintainer comment identifying a fixing commit and crediting wSkeever. The fork changelog also credits the author's checkpoint mod for related dialogue fixes. The mod's public description describes current-bounty checks and corrected weapon conditions, consistent in approach with this source. Its downloadable plugin was not compared byte-for-byte or field-for-field.

No matching Neon checkpoint bounty fix was found in the USFP public version history searched during this audit. This does not establish absence from the USFP plugin.

## Implication for the reported play session

This is an existing SFCP fix to verify in the active load order, not a newly discovered missing SFCP fix. If only USFP is installed, the SFCP fork's contents say nothing about which conditions the running game uses. If SFCP is installed, verify whether these four responses survive later overrides. A current bounty in one of the checked factions is another possibility to test.

No live logs, installed plugin list, current vanilla records, or winning overrides were inspected. The pasted log conclusions are context, not independently verified observations. No mods were installed and no gameplay files changed.

Next bounded step: inspect winning overrides for these four INFO records and check the corresponding current bounty values. Do not install a whole second overhaul patch solely to address this dialogue issue.

## Sources

- [Issue 319](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/issues/319).
- [Maintainer confirmation](https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/issues/319#issuecomment-1772653152).
- [Fork response records](https://github.com/thatRALLiguy/Starfield-Community-Patch/tree/0ad97d3eb087dafb91afbc4bbb1588598212cc87/spriggit/Quests/DialogueNeonConvo_SecurityCheckpoint%20-%2032C7C0_Starfield.esm/DialogTopics/32C7C3_Starfield.esm/Responses).
- [Security Checkpoints Dialog Fixes](https://www.nexusmods.com/starfield/mods/5724).
- [USFP version history](https://www.afkmods.com/Unofficial%20Starfield%20Patch%20Version%20History.html).
