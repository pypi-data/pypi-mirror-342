# Changelog

---

## [v4.2.0](https://bitbucket.org/jdufour/phystool/commits/tag/v4.2.0) - 2025-04-18

### Features

- [d370967](https://bitbucket.org/jdufour/phystool/commits/d37096759db01e93dfa85f706a1c134e03c66fbf) *(tool)* Cli as a new --about option

### Miscellaneous

- [fd2443a](https://bitbucket.org/jdufour/phystool/commits/fd2443a99aea593115acba9d82a346d91c3ef45f) *(noob)* Remove dock titles (Filtres, Liste)

### Documentation

- [65de354](https://bitbucket.org/jdufour/phystool/commits/65de354d789c5720e40416556d837e55475ff8f5) General improvement
- [4761ced](https://bitbucket.org/jdufour/phystool/commits/4761ced7f564af87387be7d2aea77ff64bfe12d9) Start LaTeX documentation


---

## [v4.1.0](https://bitbucket.org/jdufour/phystool/commits/tag/v4.1.0) - 2025-04-15

### Miscellaneous

- [561ea52](https://bitbucket.org/jdufour/phystool/commits/561ea5248b6780683bc93b407b3f2f5cef8981ed) *(tool)* Use bat to display texfile in terminal

### Documentation

- [574b0e4](https://bitbucket.org/jdufour/phystool/commits/574b0e4509e294b8880c68c7c4cc6688d5b3aeed) Write a more complete introduction
- [921261a](https://bitbucket.org/jdufour/phystool/commits/921261a6a7152ae684fd84742b47fd65187c588f) Add changelog to readthedocs
- [6f2c9db](https://bitbucket.org/jdufour/phystool/commits/6f2c9dbfab0f3789c896892d606c3a29cbc1ff0c) Use sphinx-autodoc2

### Revert

- [0ca9447](https://bitbucket.org/jdufour/phystool/commits/0ca944726aba6b2bf9b65cf9b0286b28cdf48432) *(noob)* Changelog and readme replaced by about


---

## [v4.0.0](https://bitbucket.org/jdufour/phystool/commits/tag/v4.0.0) - 2025-04-10

### Bug Fixes

- [526fbee](https://bitbucket.org/jdufour/phystool/commits/526fbeebec0bc2bdb4f714eb914789fa6b212653) Ensure Tags doesn't contain an empty category
- [9e2fe3b](https://bitbucket.org/jdufour/phystool/commits/9e2fe3b2e2775912b25497e5693cc30981e4cc25) *(noob)* QClipboard -> QGuiApplication.clipboard()
- [811769f](https://bitbucket.org/jdufour/phystool/commits/811769fa6a37711b230c209c691df86782b646c1) *(tool)* PDBFile.zip() Figure inclusion

### Refactor

- [b171abd](https://bitbucket.org/jdufour/phystool/commits/b171abd10d5757da3cd26198d53636e049c1be46) Move MultipleSelectionWidget in qt.helper
- [f939aac](https://bitbucket.org/jdufour/phystool/commits/f939aac258e4c1f7c13e94cc2c65820a45e8f8ce) Merge Metadata.uuid_search in Metadata.filter
- [260ec06](https://bitbucket.org/jdufour/phystool/commits/260ec060da5f5e3cd0ff50dde0dc67197bf6def5) Get_new_pdb_filename -> new_pdb_filename
- [3a5c9cc](https://bitbucket.org/jdufour/phystool/commits/3a5c9cc294672add74b0d69a065cd04d2aa7f7be) *(tool)* Split CLI in subcommands


### Miscellaneous

- [deca506](https://bitbucket.org/jdufour/phystool/commits/deca506cddac98bb58c8258778fa632ca2d8bfeb) Improve Tags.validate (strip whitespace)
- [ecfd874](https://bitbucket.org/jdufour/phystool/commits/ecfd874ef6fb814366ef8bccf60a711d9a7c663c) Allow different loglevel in dev

### Documentation

- [a4dc12c](https://bitbucket.org/jdufour/phystool/commits/a4dc12cabd0d36107abfe07ed430a3f979cd5bca) Improve documentation, add link to readthedocs
- [0a1137c](https://bitbucket.org/jdufour/phystool/commits/0a1137c803db7cff498c3f8424ed89623f292763) Improve general documentation
- [b918492](https://bitbucket.org/jdufour/phystool/commits/b9184929b2cc841ccc1fd060ac923fbd3964b4c0) Sphinx reads  version from \_\_about\_\_.py
- [cc2155b](https://bitbucket.org/jdufour/phystool/commits/cc2155b2ea4a2c68472d915dfab23880120c8d4f) Partial CLI documentation


---

## [v3.3.2](https://bitbucket.org/jdufour/phystool/commits/tag/v3.3.2) - 2025-03-31

### Bug Fixes

- [c21fe1f](https://bitbucket.org/jdufour/phystool/commits/c21fe1f6ad997f02cf04f846a7c1a60502ec301b) Tags filtering
- [c01593b](https://bitbucket.org/jdufour/phystool/commits/c01593bdd4b3ae79984e185f851994bf3d0445df) Add --max-depth=1 to ripgrep search

### Refactor

- [069e478](https://bitbucket.org/jdufour/phystool/commits/069e478200c4cef550f6c7727c90e81870d54f64) Shorter config variables

### Miscellaneous

- [5bc9aef](https://bitbucket.org/jdufour/phystool/commits/5bc9aef717ddee0e7ffe133e224cdc520359e4d5) Improve Tags (Tags() is invalid, more tests)
- [1dd0a57](https://bitbucket.org/jdufour/phystool/commits/1dd0a57d8b05432dd5f2bcd258062941768fcf6e) Various small fixes
- [a8d10ec](https://bitbucket.org/jdufour/phystool/commits/a8d10ec8cf290c950efb1401471bd2a84752685a) *(tool)* Replace search by filter

### Documentation

- [896bd67](https://bitbucket.org/jdufour/phystool/commits/896bd67f3c57a08ae2942d14decd16f06276ae11) Improve readthedocs


---

## [v3.3.1](https://bitbucket.org/jdufour/phystool/commits/tag/v3.3.1) - 2025-03-26

### Bug Fixes

- [e742297](https://bitbucket.org/jdufour/phystool/commits/e742297fafb55c52ef3e95142b6e8710586eb569) Pyproject CHANGELOG bump


---

## [v3.3.0](https://bitbucket.org/jdufour/phystool/commits/tag/v3.3.0) - 2025-03-26

### Documentation

- [d146f05](https://bitbucket.org/jdufour/phystool/commits/d146f05bcc6fc3f386129ec48592f37ddb1dc275) Improve sphinx configuration


---

## [v3.2.0](https://bitbucket.org/jdufour/phystool/commits/tag/v3.2.0) - 2025-03-26

### Bug Fixes

- [c38bb0d](https://bitbucket.org/jdufour/phystool/commits/c38bb0d9453a0f1fdf5dcfcd7a7708036c2eda76) Git api key won't automatically deprecate

### Miscellaneous

- [eba282a](https://bitbucket.org/jdufour/phystool/commits/eba282a0c4c4507c88bb482d57af4ce79fad67a8) Git diff with delta sets --tabs=4
- [81a5a8b](https://bitbucket.org/jdufour/phystool/commits/81a5a8b7c641de20ab809050f97baa3f95ea322d) Improve git error/warning messages
- [b4c76ee](https://bitbucket.org/jdufour/phystool/commits/b4c76ee2c2ea4ed87d4b2829554270986cfa65fa) *(noob)* Add busy progress bar during git push

### Documentation

- [e3d5cd4](https://bitbucket.org/jdufour/phystool/commits/e3d5cd48a00f542cb1df91d575b84ebedc5bdc67) Setup readthedocs


---

## [v3.1.0](https://bitbucket.org/jdufour/phystool/commits/tag/v3.1.0) - 2025-03-14

### Features

- [8e152a4](https://bitbucket.org/jdufour/phystool/commits/8e152a468b61e70ae6471e8710db326777fd2bdf) Add progress bar during consolidation process

### Miscellaneous

- [6016a5e](https://bitbucket.org/jdufour/phystool/commits/6016a5e14e978a364cfbef0afddbf33447d57f1b) Metadata field "figures" only contains uuids
- [365c70f](https://bitbucket.org/jdufour/phystool/commits/365c70f32b3e37932ed84cc8a2417a92e4fb3398) Speed improvement in git diff analysis


---

## [v3.0.0](https://bitbucket.org/jdufour/phystool/commits/tag/v3.0.0) - 2025-03-12

### Features

- [eacd054](https://bitbucket.org/jdufour/phystool/commits/eacd054b3f75b0a0eb5b161b5b30b8f32dd43160) *(noob)* Implement git interface
  > **breaks** The new git tool require two `bat` and `delta` to properly run git (see README.md). Moreover, a new "[git]" section is required in `~/.phystool/phystool.conf`. It needs to contain and empty  field "theme =" that will automatically be configured



---

## [v2.9.0](https://bitbucket.org/jdufour/phystool/commits/tag/v2.9.0) - 2025-03-10

### Miscellaneous

- [fe5e53f](https://bitbucket.org/jdufour/phystool/commits/fe5e53f605bc5c68a83875b22ebe0f98332a92a5) LatexLogParser catches pdf page inclusion
- [d5a0e51](https://bitbucket.org/jdufour/phystool/commits/d5a0e51a88c7edce8828a4254cf75710d20d747d) LatexLogParser catches illegal unit of measure
- [d45a3b7](https://bitbucket.org/jdufour/phystool/commits/d45a3b7fd953dbab9b6083a5d445dfc086dee048) *(noob)* Initial layout has filters on top


---

## [v2.8.1](https://bitbucket.org/jdufour/phystool/commits/tag/v2.8.1) - 2025-03-07

### Bug Fixes

- [74b44ac](https://bitbucket.org/jdufour/phystool/commits/74b44aca9a74913cde6a1a9f4b03be9628c87b3f) Ensure config dir exists
- [1791849](https://bitbucket.org/jdufour/phystool/commits/1791849398941b2e9e39cf92344198eaca05ee7f) Remove unused tag categories
- [d65cf25](https://bitbucket.org/jdufour/phystool/commits/d65cf254c6658067912ebffbdae8afe292025c57) *(noob)* Update correct column after tag modification


---

## [v2.8.0](https://bitbucket.org/jdufour/phystool/commits/tag/v2.8.0) - 2025-03-05

### Features

- [a1162c6](https://bitbucket.org/jdufour/phystool/commits/a1162c6c61399e4ae0f361dad816e7767aa35129) *(noob)* Can save/restore layout and filters


---

## [v2.7.0](https://bitbucket.org/jdufour/phystool/commits/tag/v2.7.0) - 2025-03-04

### Features

- [809fcf7](https://bitbucket.org/jdufour/phystool/commits/809fcf7cc5c418bd6f1bdb204033f6243f38071b) *(noob)* The side wigdets are now docked
- [4416e5b](https://bitbucket.org/jdufour/phystool/commits/4416e5b1a8374bffb5dc0c331913f2f4bf4cc5f7) *(noob)* Replace logger by smarter error message

### Miscellaneous

- [fef751e](https://bitbucket.org/jdufour/phystool/commits/fef751ef6fce83154578b3c2ac13b948f9e202fe) Explain how to include figures in tex


---

## [v2.6.0](https://bitbucket.org/jdufour/phystool/commits/tag/v2.6.0) - 2025-03-02

### Features

- [c62b7f8](https://bitbucket.org/jdufour/phystool/commits/c62b7f8aa3d82b49b826e069548afe4540c80be4) *(noob)* Selected uuids can be copied to cipboard

### Bug Fixes

- [b3743f5](https://bitbucket.org/jdufour/phystool/commits/b3743f53eede14582339af4d9ed2cfd58c4d8ef9) *(noob)* Handle SSLError on CHANGELOG.md download

### Miscellaneous

- [7e0ea20](https://bitbucket.org/jdufour/phystool/commits/7e0ea20f0296a0e5d31718c790ff4b6a64697fc7) Ripgrep uses smart case, rapidfuzz keeps symbols

### Revert

- [b494aad](https://bitbucket.org/jdufour/phystool/commits/b494aad449342237e09019940c09910fec47ac60) PDBFile.should_compile no longer checks figures


---

## [v2.5.2](https://bitbucket.org/jdufour/phystool/commits/tag/v2.5.2) - 2025-02-24

### Bug Fixes

- [1e4c8da](https://bitbucket.org/jdufour/phystool/commits/1e4c8da149d59ce856b380b60593535ca7e1fea8) Add requests to pyproject requirements


---

## [v2.5.1](https://bitbucket.org/jdufour/phystool/commits/tag/v2.5.1) - 2025-02-24

### Bug Fixes

- [d9e066d](https://bitbucket.org/jdufour/phystool/commits/d9e066df50645ab3d2943d2609d0ca679c460610) *(noob)* Request CHANGELOG.md with app passord


---

## [v2.5.0](https://bitbucket.org/jdufour/phystool/commits/tag/v2.5.0) - 2025-02-23

### Features

- [c668583](https://bitbucket.org/jdufour/phystool/commits/c66858343856555f31b79388a2765a098cd93022) *(noob)* Fuzzy title search colors matches


---

## [v2.4.0](https://bitbucket.org/jdufour/phystool/commits/tag/v2.4.0) - 2025-02-22

### Features

- [f102a45](https://bitbucket.org/jdufour/phystool/commits/f102a45332168237dd000b134f18a1f6d86d9953) *(noob)* Can perform fuzzy search on titles

### Bug Fixes

- [bcaf85e](https://bitbucket.org/jdufour/phystool/commits/bcaf85e863d1cece8fe1c851a989a4323df56ee5) Hatch push script

### Miscellaneous

- [2c4f6bb](https://bitbucket.org/jdufour/phystool/commits/2c4f6bb3fb316c6822680a581c43e7fedf385090) *(noob)* Use french labels


---

## [v2.3.0](https://bitbucket.org/jdufour/phystool/commits/tag/v2.3.0) - 2025-02-19

### Features

- [0905b26](https://bitbucket.org/jdufour/phystool/commits/0905b267e6d40d4529f84dbedf31c0b40310d8cb) *(noob)* Auto compile when tex_file changes

### Test

- [7de89b0](https://bitbucket.org/jdufour/phystool/commits/7de89b01d4632fb015699166212eeb7cd10ec2d6) Correct ripgrep test

### Miscellaneous

- [64cacb8](https://bitbucket.org/jdufour/phystool/commits/64cacb8486a1aad3134b7c00301ae0c0aad4ea9d) Configure hatch to automatically bump version
- [176797b](https://bitbucket.org/jdufour/phystool/commits/176797b8244f90a5aa8931c309c3bcaf5a917a53) *(noob)* Prevents process duplication
- [804464e](https://bitbucket.org/jdufour/phystool/commits/804464ec55326a20f6dd4f2529e81100822a61b1) *(noob)* Logger set CenterOnScroll and MaximumBlock
- [65284e3](https://bitbucket.org/jdufour/phystool/commits/65284e34d71e2ea9f47eab2fa2b39321cc9cc920) *(noob)* Simplify pdf widget
- [5ba20a7](https://bitbucket.org/jdufour/phystool/commits/5ba20a73eac7eed6171c534f811f16687f2985c8) Improve hatch configuration


---

## [v2.2.0](https://bitbucket.org/jdufour/phystool/commits/tag/v2.2.0) - 2025-02-19

### Features

- [36b6806](https://bitbucket.org/jdufour/phystool/commits/36b6806c89672078096f87d1b8028a6a5c13892a) *(noob)* Move logs and add compilation button


---

## [v2.1.1](https://bitbucket.org/jdufour/phystool/commits/tag/v2.1.1) - 2025-02-19

### Bug Fixes

- [c0b92ed](https://bitbucket.org/jdufour/phystool/commits/c0b92edc55ecfbe9e65a68acc0a3d2f2eee93547) *(noob)* Fix regression when creating new file


---

## [v2.1.0](https://bitbucket.org/jdufour/phystool/commits/tag/v2.1.0) - 2025-02-19

### Features

- [d9a64cd](https://bitbucket.org/jdufour/phystool/commits/d9a64cd1b4824c54028655c1febc7d10c6445e17) *(noob)* Add version in title bar
- [6452eb4](https://bitbucket.org/jdufour/phystool/commits/6452eb4b87c2e09d28dcf7c11d0b90b816506794) *(noob)* Accept other editor than kile or vim

### Bug Fixes

- [fa73c8d](https://bitbucket.org/jdufour/phystool/commits/fa73c8dd90ae227959f4587b20bcd7741cc177e1) *(noob)* Warns if opening the editor fails

### Test

- [db01f8a](https://bitbucket.org/jdufour/phystool/commits/db01f8ab09dbac83bc439fb697d2df2a56977322) Improve test for latex undefined command

### Miscellaneous

- [faeb866](https://bitbucket.org/jdufour/phystool/commits/faeb86677fc27372448e9f85054efba06b1a35c3) LatexLogParser.VERBOSE can be toggled
- [1297b58](https://bitbucket.org/jdufour/phystool/commits/1297b58e98778914e34729ca35f492a00772f501) *(noob)* Reorganise menu


---

## [v2.0.1](https://bitbucket.org/jdufour/phystool/commits/tag/v2.0.1) - 2025-02-19

### Bug Fixes

- [e2ea971](https://bitbucket.org/jdufour/phystool/commits/e2ea971f4f74d43f6a39ff143c3e8a1bed765904) Latex log parser replaces problematic characters

### Documentation

- [28b366d](https://bitbucket.org/jdufour/phystool/commits/28b366dd2a97e40ce561fa2e0d28aa49ce01306a) Simplify latex documentclass


---

## [v2.0.0](https://bitbucket.org/jdufour/phystool/commits/tag/v2.0.0) - 2025-02-19

### Features

- [1cf8e59](https://bitbucket.org/jdufour/phystool/commits/1cf8e598201f36fa3b7f097fc40df666c6f07b81) Latex can handle pdftex error
- [1c61602](https://bitbucket.org/jdufour/phystool/commits/1c61602756d7efbdc77df9c268e850d6b6c81c4a) PDBFile.should_compile also checks figures
- [b0be0e1](https://bitbucket.org/jdufour/phystool/commits/b0be0e11f6065861b04c14a049e021fdd0b42f5d) *(noob)* Creates default DB if it's not found
- [37a5a7e](https://bitbucket.org/jdufour/phystool/commits/37a5a7eda848713954635a947433070d3cbcf59d) *(noob)* Add about menu with readme and changelog

### Bug Fixes

- [5fc0101](https://bitbucket.org/jdufour/phystool/commits/5fc010183b17f734d6bb917536bfe7897f4d40e4) Remove double compilation at startup
- [806904b](https://bitbucket.org/jdufour/phystool/commits/806904babb7448c19f48fde47dc42b15809fc097) Theory.update failed to find PdbTikz
- [1b9f831](https://bitbucket.org/jdufour/phystool/commits/1b9f8310e72a4cdda2cf69cc111dd538fe49fee7) LatexLogParser catches long missing File
- [8ba449b](https://bitbucket.org/jdufour/phystool/commits/8ba449b0c71ac7653b05ec0938b36a0f5134f4ce) LatexLogParser local file detection has changed
- [eeb712e](https://bitbucket.org/jdufour/phystool/commits/eeb712ede5a7970f7cdb54e1907096557c58f21c) *(noob)* ProcessManager should not loose processes
- [916097d](https://bitbucket.org/jdufour/phystool/commits/916097dc18e7587ca5fc9fc91e485a56997ad9ea) *(noob)* Update filters after consolidation
- [78b7d52](https://bitbucket.org/jdufour/phystool/commits/78b7d52d7eb43086a60e3df5fe60fc1ee7a9e2a9) *(noob)* Remove warning on cancelled file import

### Refactor

- [8cb3d3b](https://bitbucket.org/jdufour/phystool/commits/8cb3d3b24f08cde25fa8ce310e145a724e7a98a8) Simplify configuration file
  > **breaks** The configuration file is simpler. It only allows a documentclass for figures and a common one for all other file types. As the documentclass doesn't take options, the database path must be set via the command `\PdbSetDBPath{/path/to/db}`. This command is automatically added to the header of the temporary *texfile* generated by *physnoob* at compilation.

- [db7aa4f](https://bitbucket.org/jdufour/phystool/commits/db7aa4fc3264345f0bc34688f9abe3242c33b7a5) New configuration file name and structure
  > **breaks** The configuration file is now `~/.phystool/phystool.conf` and must but in the INI format.


### Miscellaneous

- [832f600](https://bitbucket.org/jdufour/phystool/commits/832f6006c50ebf4382b2fc0fbd7ed71fd6375a54) Improve PDBFile.\_\_str\_\_
- [c123349](https://bitbucket.org/jdufour/phystool/commits/c123349b5ae1b951c75121a7c7f4b0b71b7dee11) Config.py Exception -> ModuleNotFoundError
- [7fd3e96](https://bitbucket.org/jdufour/phystool/commits/7fd3e9674db1ca400a9f8bf8b81265c7a8eead55) Latex.compilation_command unifies command

### Documentation

- [2212d08](https://bitbucket.org/jdufour/phystool/commits/2212d08cd30ca6992d0312d659de01894c9f29f0) Use git-cliff to create changelog
- [2e2499b](https://bitbucket.org/jdufour/phystool/commits/2e2499bdeadd9877887e1edbd7770e1a203493fb) Configure git-cliff
- [5b5241d](https://bitbucket.org/jdufour/phystool/commits/5b5241d26b26b6bb26ddb6861bfa4dc723e97dc7) Improve README.md


---

## [v1.3.0](https://bitbucket.org/jdufour/phystool/commits/tag/v1.3.0) - 2025-02-12

### Features

- [88829d6](https://bitbucket.org/jdufour/phystool/commits/88829d69ec1022f8bd96e5b26daede6a688462f3) Can remove PDBFile -> refactoring required

### Bug Fixes

- [f7c56c7](https://bitbucket.org/jdufour/phystool/commits/f7c56c7562c4c919f5b8b4817c40245f84dbf158) Replace ag by ripgrep

### Test

- [0a5be58](https://bitbucket.org/jdufour/phystool/commits/0a5be58e9a43e9b45692dada87b798193c792d88) Add latex test function for warning

### Miscellaneous

- [353f93f](https://bitbucket.org/jdufour/phystool/commits/353f93f79dfd384c7ee57f09be5a4a79ab5f78ef) Tags.\_\_str\_\_ doesn't return brackets

### Documentation

- [4d03245](https://bitbucket.org/jdufour/phystool/commits/4d032457bf90f8510acf9630f532287af3d7dd5c) Fix typo
- [9342ef2](https://bitbucket.org/jdufour/phystool/commits/9342ef29e08d329fd1a5acc9adf09da19edb6e5c) Replace ag by ripgrep in README.md


---

## [v1.2.0](https://bitbucket.org/jdufour/phystool/commits/tag/v1.2.0) - 2025-02-12

### Features

- [6438f0a](https://bitbucket.org/jdufour/phystool/commits/6438f0ad3e92b9a354a220820e51e12042dad22c) Ag can match dollars

### Test

- [8df9c21](https://bitbucket.org/jdufour/phystool/commits/8df9c218f70d994966859a533c5cdee53e3f2c34) Ag improve test cases (add é and è)

### Miscellaneous

- [0dc5212](https://bitbucket.org/jdufour/phystool/commits/0dc5212b4f840392ca38ea57ab6957adb3dc212b) *(noob)* Improve logging compilation messages

### Documentation

- [8197865](https://bitbucket.org/jdufour/phystool/commits/8197865a0f039fff67ba91ea98cd58fef0c94cf5) README informs about texmf.cnf


---

## [v1.1.1](https://bitbucket.org/jdufour/phystool/commits/tag/v1.1.1) - 2025-02-12

### Bug Fixes

- [cfc1d07](https://bitbucket.org/jdufour/phystool/commits/cfc1d0731aa76565971416ee27c9760505353683) Ag is now case insensitive
- [85dfde7](https://bitbucket.org/jdufour/phystool/commits/85dfde7e49bafa03e3dc73b352c196658808bcdd) *(noob)* Recovers from corrupted DB after restart
- [e7633a3](https://bitbucket.org/jdufour/phystool/commits/e7633a306058674ebd65067ed43fe1cf67cd2716) *(noob)* Starts from scratch (no tex files)
- [4505560](https://bitbucket.org/jdufour/phystool/commits/450556002ddda60621d800e1b4f815e535946276) Ag handles correctly backslashes

### Miscellaneous

- [cb80fcd](https://bitbucket.org/jdufour/phystool/commits/cb80fcdb63342964f695bfd449e4889567a21b7b) *(noob)* Change PdbFileListWidget constructor


---

## [v1.1.0](https://bitbucket.org/jdufour/phystool/commits/tag/v1.1.0) - 2025-02-12

### Features

- [495d8b1](https://bitbucket.org/jdufour/phystool/commits/495d8b1f99da6024cde63e725c5fe128157d0a0e) *(noob)* Can create an empty new file

### Bug Fixes

- [249a853](https://bitbucket.org/jdufour/phystool/commits/249a8532248b0baa8ab99c45631d713fe5d37398) Ag searches strings with backslash
- [f1af7d3](https://bitbucket.org/jdufour/phystool/commits/f1af7d3520c98a581e8b39ce1334d12492aaf2eb) Metadata.filter doesn't exclude empty tags

### Refactor

- [c5ef5a3](https://bitbucket.org/jdufour/phystool/commits/c5ef5a349fe2ba6983cba569c05483aa3a830e5d) Define qt.process.process_open_files
- [8f9aa08](https://bitbucket.org/jdufour/phystool/commits/8f9aa08f03f4cb6e03a13a6b40972933b81717bc) PDBFile.open_unkown loops through available PDBFile

### Miscellaneous

- [e84f83c](https://bitbucket.org/jdufour/phystool/commits/e84f83cc6c586b5487b8be4b8b3f0337e76bc9a5) *(noob)* Rename qt.pdbfile method
- [ececa00](https://bitbucket.org/jdufour/phystool/commits/ececa00408a12ba4dd55116c6c3970a5a64e40fc) Hatch auto increment version in \_\_about.py\_\_

### Documentation

- [d0ee911](https://bitbucket.org/jdufour/phystool/commits/d0ee9115141a240f0fa4a878d0d856535cda1546) Add CHANGELOG
- [62f2bcf](https://bitbucket.org/jdufour/phystool/commits/62f2bcf9413917298c3092db68e5b1dfca912484) Improve git-changelog configuration
- [0fcafcb](https://bitbucket.org/jdufour/phystool/commits/0fcafcbc075fbe0f2ba3e4e9eaaa1b8afba53e1f) Remove section in pyproject.toml
- [3912538](https://bitbucket.org/jdufour/phystool/commits/3912538827433a3cfb5a0312b854c3414db2dbce) Change git-changelog versionning to pep440
- [99b6798](https://bitbucket.org/jdufour/phystool/commits/99b6798184ba965db710180ab000e150e4efe21e) CHANGELOG.md should increment correctly
- [4e5e719](https://bitbucket.org/jdufour/phystool/commits/4e5e719d2050fe4c1b51930922db381594bdbcb9) Improve git-changelog configuration


---

## [v1.0.0](https://bitbucket.org/jdufour/phystool/commits/tag/v1.0.0) - 2025-02-12

### Features

- [d59e01e](https://bitbucket.org/jdufour/phystool/commits/d59e01efa13e075e5c797ffb870a9a4febae93a8) *(noob)* Can open tex_files in custom editor
- [76ba436](https://bitbucket.org/jdufour/phystool/commits/76ba436927dfbdbfd072b98945fc9aec8830f0cc) *(noob)* Double click to edit, Ctrl-E to tag
- [55d325a](https://bitbucket.org/jdufour/phystool/commits/55d325af926201885ad82f25764de9acdbf6bd62) *(noob)* Can edit tags in bulk

### Bug Fixes

- [8633fe6](https://bitbucket.org/jdufour/phystool/commits/8633fe65b89b22423ef88adfcf6706b5901a3d38) *(noob)* Item label when changing tags
- [681e5c9](https://bitbucket.org/jdufour/phystool/commits/681e5c9a1db2f53d22c50a5bdefc7486f42e5042) *(noob)* Manage processes
- [cb900a1](https://bitbucket.org/jdufour/phystool/commits/cb900a1921e9f1873d61804b68123bca5e604154) *(noob)* Display for background compilation
- [3c91e77](https://bitbucket.org/jdufour/phystool/commits/3c91e7763bd9f1beefc9462f653513310c658ce3) *(noob)* File opening currupts config arguments

### Miscellaneous

- [45b971d](https://bitbucket.org/jdufour/phystool/commits/45b971db6fd659454e802590608d41032afd1ac4) *(noob)* Rename variable

<!-- generated by git-cliff -->
