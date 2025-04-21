# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.7.1](https://github.com/arot-devs/procslib/releases/tag/0.7.1) - 2025-04-20

<small>[Compare with 0.7.0](https://github.com/arot-devs/procslib/compare/0.7.0...0.7.1)</small>

### Bug Fixes

- typo ([e425e9a](https://github.com/arot-devs/procslib/commit/e425e9a2b6bc3f277f72f0ce7ce78cfa38ab1b77) by yada).

### Code Refactoring

- organizing models ([888b792](https://github.com/arot-devs/procslib/commit/888b7926002f44d3679e46a40c0188f791dddf2b) by yada).
- properly naming models ([fb70b50](https://github.com/arot-devs/procslib/commit/fb70b501fe1d5bdac56033aa63ab13552e7dda35) by yada).

## [0.7.0](https://github.com/arot-devs/proclib/releases/tag/0.7.0) - 2025-03-11

<small>[Compare with 0.6.0](https://github.com/arot-devs/proclib/compare/0.6.0...0.7.0)</small>

### Features

- adding working camie tagger implementation ([479f385](https://github.com/arot-devs/proclib/commit/479f385d54068426da8504df13c30a300d653326) by yada).
- adding working camie tagger inference ([d99984e](https://github.com/arot-devs/proclib/commit/d99984e2b36b41e3a0ccdc7aeea49c2bb46b98e3) by yada).
- adding batch infer script (for 8card setups) ([9f99003](https://github.com/arot-devs/proclib/commit/9f990031f86b3ae3a80356bd7fdc21615121fa62) by yada).

## [0.6.0](https://github.com/arot-devs/proclib/releases/tag/0.6.0) - 2025-03-07

<small>[Compare with 0.5.0](https://github.com/arot-devs/proclib/compare/0.5.0...0.6.0)</small>

### Features

- adding pixai tagger inference ([2fea244](https://github.com/arot-devs/proclib/commit/2fea244d4604db2635877ceb49cb135304a1ca06) by yada).
- adding novelai generator ([ff4cabd](https://github.com/arot-devs/proclib/commit/ff4cabd971d74391b96e992f5a12e2af160fc63a) by yada).
- adding fiftyone eval code; modifying automodel config ([97efd4d](https://github.com/arot-devs/proclib/commit/97efd4d6d64b2c19c5d8d8af985d0b73a53d3379) by yada).
- UniboxImagePathDataset (works with s3/url)! ([d813c6d](https://github.com/arot-devs/proclib/commit/d813c6d8b66982824bc1455beaae0b2abc0b02d8) by yada).
- wdv3 tagger inference class ([feb1e20](https://github.com/arot-devs/proclib/commit/feb1e20642a8877a05ac34f23b85843219b99208) by yada).

### Bug Fixes

- missing dependency ([e28df31](https://github.com/arot-devs/proclib/commit/e28df31bbee196cb4b527404b2ddeadae54b599c) by yada).

### Code Refactoring

- using general hf inference class for aigc cls ([7d4bb2c](https://github.com/arot-devs/proclib/commit/7d4bb2cc2c1d7343bd0e15a8dfbd37996ecfb494) by yada).
- using general hf inference class for anime real cls ([1241997](https://github.com/arot-devs/proclib/commit/1241997d1a712e88cf7218ee02e656b5db5414d0) by yada).
- adding unified hf automodel inference class ([bb39741](https://github.com/arot-devs/proclib/commit/bb397417e07da31e91eaac50c8002c3713b38340) by yada).

## [0.5.0](https://github.com/arot-devs/proclib/releases/tag/0.5.0) - 2025-02-13

<small>[Compare with 0.4.2](https://github.com/arot-devs/proclib/compare/0.4.2...0.5.0)</small>

### Features

- adding nsfw classifier into procslib ([f50e6bf](https://github.com/arot-devs/proclib/commit/f50e6bf7a9d1f6af3acd3aa327fce9ddb56ec6d1) by yada).
- adding new models: aigc classifier; jz tagger; image category classifier ([00a6cb2](https://github.com/arot-devs/proclib/commit/00a6cb26b1c0db390edef141fe401606681d8ffc) by yada).
- adding hf tools for file transfer ([6f1f0e3](https://github.com/arot-devs/proclib/commit/6f1f0e357d21ae4ffeaf9a3d894a8470d8a6589d) by yada).
- adding jz tagger (baic scratch) ([c53908f](https://github.com/arot-devs/proclib/commit/c53908fbc72ceb4520501648aea51bd26dec0f9b) by yada).
- moving most of the files into huggingface ([94318ad](https://github.com/arot-devs/proclib/commit/94318ad83f5479c4bfbf2c83c5b0a79f61491949) by yada).
- adding weakm v3 model ([86537c4](https://github.com/arot-devs/proclib/commit/86537c49d74f51e26a5fb49fa2b62ef9ef7b956c) by yada).
- adding vila inference code (needs shm) ([1a46685](https://github.com/arot-devs/proclib/commit/1a466859e2597ce79a8381601ceabaa475d1a414) by yada).

### Bug Fixes

- incorrect vila wrapper code ([06be8cf](https://github.com/arot-devs/proclib/commit/06be8cfdec56ed0de381896974a3b5f9b1dc3050) by yada).

## [0.4.2](https://github.com/arot-devs/proclib/releases/tag/0.4.2) - 2024-12-26

<small>[Compare with v0.4.1](https://github.com/arot-devs/proclib/compare/v0.4.1...0.4.2)</small>

## [v0.4.1](https://github.com/arot-devs/proclib/releases/tag/v0.4.1) - 2024-12-25

<small>[Compare with 0.4.0](https://github.com/arot-devs/proclib/compare/0.4.0...v0.4.1)</small>

## [0.4.0](https://github.com/arot-devs/proclib/releases/tag/0.4.0) - 2024-12-25

<small>[Compare with 0.3.1](https://github.com/arot-devs/proclib/compare/0.3.1...0.4.0)</small>

### Features

- adding hf model download code ([b166f7e](https://github.com/arot-devs/proclib/commit/b166f7e20b0ad1530ec2c5c43e17a1d6782cf76d) by yada).
- adding clip aesthetics inference code (needs further code) ([81bf33b](https://github.com/arot-devs/proclib/commit/81bf33b23dc132921fdfaa5f722c70e33708d5b9) by yada).
- adding batch infer script for models ([d00cd82](https://github.com/arot-devs/proclib/commit/d00cd82b38a1b47309a9b188772dccb83d71ad03) by yada).

### Bug Fixes

- depth wrapper inference not using enough workers (and too high resolution) ([7205f7f](https://github.com/arot-devs/proclib/commit/7205f7f0f37107246240f05d111484bc00f45116) by yada).
- gpu naming retrieved incorrectly when using clip aesthetics inference ([109454c](https://github.com/arot-devs/proclib/commit/109454cc1debc8c2e72748ce7e06b91036b526c4) by yada).
- adding missing dependencies ([b7abf1d](https://github.com/arot-devs/proclib/commit/b7abf1d8aafa4cc15a60ac696171e5f975cdda34) by yada).
- allow dynamic imports and static type hinting using type checkers ([27a2e0f](https://github.com/arot-devs/proclib/commit/27a2e0f719026d1307954a8b0bff0a8884c29678) by yada).
- incorrect anime aesthetic inference code ([39a3979](https://github.com/arot-devs/proclib/commit/39a3979ef3542a71fdb3eb69940905449da336e7) by yada).
- pip installer issue; merge conflict ([407260e](https://github.com/arot-devs/proclib/commit/407260e22a49aeeb6c8d2bd122e055631ca21789) by yada).
- create folder during batch inference if not found ([5e76ff3](https://github.com/arot-devs/proclib/commit/5e76ff3e1bc01db0ef0831b8d88ea2cff9e5e436) by yada).
- incorrect args for infer_many script ([78c08b9](https://github.com/arot-devs/proclib/commit/78c08b986342462a2ca8ac121cfcc9123aa64d2a) by yada).

### Code Refactoring

- partially adding more inputs to model getters ([f328952](https://github.com/arot-devs/proclib/commit/f32895289b0c2d4cbf24810a57f5d6e1558b717b) by yada).
- changing model imports from model_builder to modules level ([8b9b1b8](https://github.com/arot-devs/proclib/commit/8b9b1b82948ebae31e25b7ad8f50f738ebceab63) by yada).

## [0.3.1](https://github.com/arot-devs/proclib/releases/tag/0.3.1) - 2024-12-21

<small>[Compare with 0.3.0](https://github.com/arot-devs/proclib/compare/0.3.0...0.3.1)</small>

### Features

- adding laion watermark inference class ([d096ea1](https://github.com/arot-devs/proclib/commit/d096ea1a7a17da01f1aef180112779a703d00389) by yada).
- adding async q-align code ([057a1e3](https://github.com/arot-devs/proclib/commit/057a1e380b577220f5946a7284030b3dd2eadfd1) by yada).
- adding q align inference class ([7268fad](https://github.com/arot-devs/proclib/commit/7268fad73703956e23cd2073258d8c14d8304602) by yada).
- adding depth estimation wrapper with batch inference ([93b9608](https://github.com/arot-devs/proclib/commit/93b9608dd03090634855c4711b846700dbde2b3f) by yada).

### Bug Fixes

- siglip aesthetic naming issues ([86a1419](https://github.com/arot-devs/proclib/commit/86a1419c9b0df8f0b09891145c5498081d0d3757) by yada).

## [0.3.0](https://github.com/arot-devs/proclib/releases/tag/0.3.0) - 2024-12-20

<small>[Compare with 0.2.0](https://github.com/arot-devs/proclib/compare/0.2.0...0.3.0)</small>

### Features

- adding rtmpose inference script ([e69c193](https://github.com/arot-devs/proclib/commit/e69c1938245b49c7dc4edd1d8cc4b8cf0196dad2) by yada).
- adding pixiv compound score model ([2def104](https://github.com/arot-devs/proclib/commit/2def10470d5c06234c8f4930ef18b1c4c8bc0910) by yada).
- adding centralized model repo for easier model use ([b02b866](https://github.com/arot-devs/proclib/commit/b02b866518d79d48748e3c2b0210bfc4daf1044b) by yada).

## [0.2.0](https://github.com/arot-devs/proclib/releases/tag/0.2.0) - 2024-12-17

<small>[Compare with 0.1.0](https://github.com/arot-devs/proclib/compare/0.1.0...0.2.0)</small>

### Features

- adding automated site building on push ([0958eec](https://github.com/arot-devs/proclib/commit/0958eec062177a1b382873bb02b0e556d9d0dcaf) by yada).

### Code Refactoring

- cleanup code before version commit ([2b450a7](https://github.com/arot-devs/proclib/commit/2b450a72ad3a4d366d46a9ec9e38e854e2b35275) by yada).
- removing unused files ([5d0484b](https://github.com/arot-devs/proclib/commit/5d0484b884592389b679b395b225290da3916f15) by yada).
- reanaing library from proclib to procslib for pypi compatability ([090255e](https://github.com/arot-devs/proclib/commit/090255ef8bcb5e5f928a00255da2aefac022b6fe) by yada).
- better naming conventions ([2bb5bfd](https://github.com/arot-devs/proclib/commit/2bb5bfdca1090df8c703f8488efa2cb6471045c9) by yada).
- cleaning up docstrings and code ([8c74944](https://github.com/arot-devs/proclib/commit/8c7494432306c6b9dcde968a98d5e8af65251f77) by yada).

## [0.1.0](https://github.com/arot-devs/proclib/releases/tag/0.1.0) - 2024-12-17

<small>[Compare with first commit](https://github.com/arot-devs/proclib/compare/3ba21b386fb501dcfc42f5baa5a011d499618bd1...0.1.0)</small>

### Features

- adding tested and refactored style cls simsiam model ([0b9e61d](https://github.com/arot-devs/proclib/commit/0b9e61d25f0658d5c03ae94252754d0b85887528) by yada).
- adding util script for splitting a folder and infer ([1c4438d](https://github.com/arot-devs/proclib/commit/1c4438d4285ed3efb465b7dccefa6a760983e273) by yada).
- adding batch infer script for anime aesthetics cls ([febfc0e](https://github.com/arot-devs/proclib/commit/febfc0e63b5788f5dd4ee25ce81b3f57156e5b80) by yada).
- adding anime aesthetic-cls code ([aa42d81](https://github.com/arot-devs/proclib/commit/aa42d81ba09b5153dcc484f7a98e8c642450e742) by yada).

### Bug Fixes

- adding error handling for broken images ([d6a9d9f](https://github.com/arot-devs/proclib/commit/d6a9d9f3e53a5765d286063a16515a566f285ca9) by yada).

### Code Refactoring

- chaning anime_aesthetic.py to use ABC class ([1bac68d](https://github.com/arot-devs/proclib/commit/1bac68d43d8fe952469b9eb5a8bb4fe5116dde06) by yada).
- changing representation of style_cls_simsiam (not tested yet) ([09a4f61](https://github.com/arot-devs/proclib/commit/09a4f6112f437549c9388b7f0533e8c2da8d428c) by yada).
- adding new abstract class for common model interface ([f1bc696](https://github.com/arot-devs/proclib/commit/f1bc696d5098ba1d7751f468430fc876e1118bd6) by yada).
- moving notebooks to subdir ([b709ce2](https://github.com/arot-devs/proclib/commit/b709ce2bc1a5273a69f273a8bbabf565224ec2e9) by yada).

## [v0.4.2](https://github.com/arot-devs/proclib/releases/tag/v0.4.2) - 2024-12-26

<small>[Compare with v0.4.1](https://github.com/arot-devs/proclib/compare/v0.4.1...v0.4.2)</small>

## [v0.4.1](https://github.com/arot-devs/proclib/releases/tag/v0.4.1) - 2024-12-25

<small>[Compare with 0.4.0](https://github.com/arot-devs/proclib/compare/0.4.0...v0.4.1)</small>

## [0.4.0](https://github.com/arot-devs/proclib/releases/tag/0.4.0) - 2024-12-25

<small>[Compare with 0.3.1](https://github.com/arot-devs/proclib/compare/0.3.1...0.4.0)</small>

### Features

- adding hf model download code ([b166f7e](https://github.com/arot-devs/proclib/commit/b166f7e20b0ad1530ec2c5c43e17a1d6782cf76d) by yada).
- adding clip aesthetics inference code (needs further code) ([81bf33b](https://github.com/arot-devs/proclib/commit/81bf33b23dc132921fdfaa5f722c70e33708d5b9) by yada).
- adding batch infer script for models ([d00cd82](https://github.com/arot-devs/proclib/commit/d00cd82b38a1b47309a9b188772dccb83d71ad03) by yada).

### Bug Fixes

- depth wrapper inference not using enough workers (and too high resolution) ([7205f7f](https://github.com/arot-devs/proclib/commit/7205f7f0f37107246240f05d111484bc00f45116) by yada).
- gpu naming retrieved incorrectly when using clip aesthetics inference ([109454c](https://github.com/arot-devs/proclib/commit/109454cc1debc8c2e72748ce7e06b91036b526c4) by yada).
- adding missing dependencies ([b7abf1d](https://github.com/arot-devs/proclib/commit/b7abf1d8aafa4cc15a60ac696171e5f975cdda34) by yada).
- allow dynamic imports and static type hinting using type checkers ([27a2e0f](https://github.com/arot-devs/proclib/commit/27a2e0f719026d1307954a8b0bff0a8884c29678) by yada).
- incorrect anime aesthetic inference code ([39a3979](https://github.com/arot-devs/proclib/commit/39a3979ef3542a71fdb3eb69940905449da336e7) by yada).
- pip installer issue; merge conflict ([407260e](https://github.com/arot-devs/proclib/commit/407260e22a49aeeb6c8d2bd122e055631ca21789) by yada).
- create folder during batch inference if not found ([5e76ff3](https://github.com/arot-devs/proclib/commit/5e76ff3e1bc01db0ef0831b8d88ea2cff9e5e436) by yada).
- incorrect args for infer_many script ([78c08b9](https://github.com/arot-devs/proclib/commit/78c08b986342462a2ca8ac121cfcc9123aa64d2a) by yada).

### Code Refactoring

- partially adding more inputs to model getters ([f328952](https://github.com/arot-devs/proclib/commit/f32895289b0c2d4cbf24810a57f5d6e1558b717b) by yada).
- changing model imports from model_builder to modules level ([8b9b1b8](https://github.com/arot-devs/proclib/commit/8b9b1b82948ebae31e25b7ad8f50f738ebceab63) by yada).

## [0.3.1](https://github.com/arot-devs/proclib/releases/tag/0.4.0) - 2024-12-21

<small>[Compare with 0.3.0](https://github.com/arot-devs/proclib/compare/0.3.0...0.4.0)</small>

### Features

- adding laion watermark inference class ([d096ea1](https://github.com/arot-devs/proclib/commit/d096ea1a7a17da01f1aef180112779a703d00389) by yada).
- adding async q-align code ([057a1e3](https://github.com/arot-devs/proclib/commit/057a1e380b577220f5946a7284030b3dd2eadfd1) by yada).
- adding q align inference class ([7268fad](https://github.com/arot-devs/proclib/commit/7268fad73703956e23cd2073258d8c14d8304602) by yada).
- adding depth estimation wrapper with batch inference ([93b9608](https://github.com/arot-devs/proclib/commit/93b9608dd03090634855c4711b846700dbde2b3f) by yada).

### Bug Fixes

- siglip aesthetic naming issues ([86a1419](https://github.com/arot-devs/proclib/commit/86a1419c9b0df8f0b09891145c5498081d0d3757) by yada).

## [0.3.0](https://github.com/arot-devs/proclib/releases/tag/0.3.0) - 2024-12-20

<small>[Compare with 0.2.0](https://github.com/arot-devs/proclib/compare/0.2.0...0.3.0)</small>

### Features

- adding rtmpose inference script ([e69c193](https://github.com/arot-devs/proclib/commit/e69c1938245b49c7dc4edd1d8cc4b8cf0196dad2) by yada).
- adding pixiv compound score model ([2def104](https://github.com/arot-devs/proclib/commit/2def10470d5c06234c8f4930ef18b1c4c8bc0910) by yada).
- adding centralized model repo for easier model use ([b02b866](https://github.com/arot-devs/proclib/commit/b02b866518d79d48748e3c2b0210bfc4daf1044b) by yada).

## [0.2.0](https://github.com/arot-devs/proclib/releases/tag/0.2.0) - 2024-12-17

<small>[Compare with 0.1.0](https://github.com/arot-devs/proclib/compare/0.1.0...0.2.0)</small>

### Features

- adding automated site building on push ([0958eec](https://github.com/arot-devs/proclib/commit/0958eec062177a1b382873bb02b0e556d9d0dcaf) by yada).

### Code Refactoring

- cleanup code before version commit ([2b450a7](https://github.com/arot-devs/proclib/commit/2b450a72ad3a4d366d46a9ec9e38e854e2b35275) by yada).
- removing unused files ([5d0484b](https://github.com/arot-devs/proclib/commit/5d0484b884592389b679b395b225290da3916f15) by yada).
- reanaing library from proclib to procslib for pypi compatability ([090255e](https://github.com/arot-devs/proclib/commit/090255ef8bcb5e5f928a00255da2aefac022b6fe) by yada).
- better naming conventions ([2bb5bfd](https://github.com/arot-devs/proclib/commit/2bb5bfdca1090df8c703f8488efa2cb6471045c9) by yada).
- cleaning up docstrings and code ([8c74944](https://github.com/arot-devs/proclib/commit/8c7494432306c6b9dcde968a98d5e8af65251f77) by yada).

## [0.1.0](https://github.com/arot-devs/procslib/releases/tag/0.1.0) - 2024-12-17

<small>[Compare with first commit](https://github.com/arot-devs/procslib/compare/3ba21b386fb501dcfc42f5baa5a011d499618bd1...0.1.0)</small>

### Features

- adding tested and refactored style cls simsiam model ([0b9e61d](https://github.com/arot-devs/procslib/commit/0b9e61d25f0658d5c03ae94252754d0b85887528) by yada).
- adding util script for splitting a folder and infer ([1c4438d](https://github.com/arot-devs/procslib/commit/1c4438d4285ed3efb465b7dccefa6a760983e273) by yada).
- adding batch infer script for anime aesthetics cls ([febfc0e](https://github.com/arot-devs/procslib/commit/febfc0e63b5788f5dd4ee25ce81b3f57156e5b80) by yada).
- adding anime aesthetic-cls code ([aa42d81](https://github.com/arot-devs/procslib/commit/aa42d81ba09b5153dcc484f7a98e8c642450e742) by yada).

### Bug Fixes

- adding error handling for broken images ([d6a9d9f](https://github.com/arot-devs/procslib/commit/d6a9d9f3e53a5765d286063a16515a566f285ca9) by yada).

### Code Refactoring

- chaning anime_aesthetic.py to use ABC class ([1bac68d](https://github.com/arot-devs/procslib/commit/1bac68d43d8fe952469b9eb5a8bb4fe5116dde06) by yada).
- changing representation of style_cls_simsiam (not tested yet) ([09a4f61](https://github.com/arot-devs/procslib/commit/09a4f6112f437549c9388b7f0533e8c2da8d428c) by yada).
- adding new abstract class for common model interface ([f1bc696](https://github.com/arot-devs/procslib/commit/f1bc696d5098ba1d7751f468430fc876e1118bd6) by yada).
- moving notebooks to subdir ([b709ce2](https://github.com/arot-devs/procslib/commit/b709ce2bc1a5273a69f273a8bbabf565224ec2e9) by yada).


## [0.0.1](https://github.com/arot-devs/procslib/releases/tag/0.0.1) - 2024-11-15

<small>[Compare with first commit](https://github.com/arot-devs/procslib/compare/819a1296d7bd635854e623aa717abdac37d8b0e9...0.0.1)</small>
