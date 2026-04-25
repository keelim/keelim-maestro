# Agent Codemap

- Repository: `android-support`
- Root: `/Users/keelim/Desktop/keelim-maestro/android-support`
- Generated: 2026-04-25 04:16 UTC
- Files scanned: 36
- Detected shape: Node/JavaScript

## Read First
- `AGENTS.md`
- `README.md`
- `package.json`
- `lib/index.js`
- `src/index.ts`
- `src/main.ts`

## Repository Shape
- TypeScript: 16 files
- [no extension]: 6 files
- YAML: 4 files
- JavaScript: 3 files
- Markdown: 2 files
- .json: 2 files
- .cjs: 1 files
- .xml: 1 files
- .aab: 1 files

## Entrypoints
- `lib/index.js`
- `src/index.ts`
- `src/main.ts`

## Key Directories
- `./`: 13 files; examples: `.eslintrc.cjs`, `.gitignore`, `.prettierrc`
- `__tests__/`: 11 files; examples: `__tests__/edits.test.ts`, `__tests__/index.test.ts`, `__tests__/input-validation.test.ts`
- `src/`: 8 files; examples: `src/edits.ts`, `src/index.ts`, `src/input-validation.ts`
- `.github/`: 3 files; examples: `.github/dependabot.yml`, `.github/workflows/manual-build.yml`, `.github/workflows/test.yml`
- `lib/`: 1 files; examples: `lib/index.js`

## Dependencies and Tooling
- `.github/workflows/manual-build.yml`
- `.github/workflows/test.yml`
- `AGENTS.md`
- `README.md`
- `package.json`

## Useful Commands
- npm script `build`: ncc build src/index.ts -m -o lib/
- npm script `test`: jest
- npm script `test:coverage`: jest --coverage

## Tests and Verification
- `__tests__/edits.test.ts`
- `__tests__/index.test.ts`
- `__tests__/input-validation.test.ts`
- `__tests__/io-utils.test.ts`
- `__tests__/logger.test.ts`
- `__tests__/main.test.ts`
- `__tests__/releasefiles/release.aab`
- `__tests__/signing.test.ts`
- `__tests__/whatsnew.test.ts`
- `__tests__/whatsnew/whatsnew-en-US`
- `__tests__/whatsnew/whatsnew-ko-KR`

## Symbol Landmarks
- `__tests__/edits.test.ts`: mockAndroidPublisher (L1), googleAuthCtor (L25), options (L66), logSpy (L78), explicitNotes (L237), result (L238), root (L363), buffer (L383)
- `__tests__/index.test.ts`: runMock (L8)
- `__tests__/input-validation.test.ts`: testValues (L4), testValues (L11), testValues (L22), testValues (L31), testValues (L36), testValues (L43), testValues (L50), testValues (L57)
- `__tests__/io-utils.test.ts`: logSpy (L12), files (L30)
- `__tests__/logger.test.ts`: debugSpy (L12), errorSpy (L13), infoSpy (L14), warnSpy (L15)
- `__tests__/main.test.ts`: setInputs (L77)
- `__tests__/signing.test.ts`: originalAndroidHome (L29), originalBuildToolsVersion (L30), result (L47)
- `__tests__/whatsnew.test.ts`: texts (L4)
- `lib/index.js`: a (L4)
- `src/edits.ts`: runUpload (L52), auth (L67), result (L71), uploadToPlayStore (L99), url (L107), appEditId (L112), versionCodes (L118), url (L122)
- `src/input-validation.ts`: validateUserFraction (L14), validateStatus (L33), validateInAppUpdatePriority (L64), validateReleaseFiles (L79), files (L83)
- `src/main.ts`: run (L29), type (L31), uploadRun (L58), serviceAccountJson (L61), serviceAccountJsonRaw (L62), packageName (L63), releaseFile (L64), releaseFilesInput (L65)
- `src/signing.ts`: signApkFile (L24), buildToolsVersion (L34), androidHome (L35), buildTools (L36), zipAlign (L41), alignedApkFile (L45), apkSigner (L54), signedApkFile (L58)
- `src/whatsnew.ts`: readLocalizedReleaseNotes (L20), releaseNotes (L24), pattern (L25), matches (L31), lang (L34), filePath (L35), content (L36)
- `src/utils/io-utils.ts`: findReleaseFiles (L3), releaseFiles (L4)
- `src/utils/logger.ts`: d (L3), e (L8), i (L13), w (L18)

## Open Questions
- No existing `docs/CODEMAPS/*` files were found.
