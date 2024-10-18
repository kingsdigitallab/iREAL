

## [0.5.3](https://github.com/jmiguelv/iREAL/compare/v0.5.2...v0.5.3) (2024-10-18)

## [0.5.2](https://github.com/jmiguelv/iREAL/compare/v0.5.1...v0.5.2) (2024-10-11)


### Bug Fixes

* **frontend:** clarify about issues with the example questions ([0d2d2dd](https://github.com/jmiguelv/iREAL/commit/0d2d2dde1b3fc4e68507bf0ff7d5d85bbe35c4d4))
* **frontend:** rename chatbot to explorer ([cc3fb6d](https://github.com/jmiguelv/iREAL/commit/cc3fb6dfa12aeceaeb4d25042db28809bee4ef14))


### Features

* **frontend:** add disclaimer and moved version and github links to the footer ([8834708](https://github.com/jmiguelv/iREAL/commit/8834708cf4083392b9ed2f84f41b0255d5445b2d))

## [0.5.1](https://github.com/jmiguelv/iREAL/compare/v0.5.0...v0.5.1) (2024-10-02)


### Bug Fixes

* **frontend:** typo ([0b04525](https://github.com/jmiguelv/iREAL/commit/0b04525788e09fc1dcf05efd80c6fae0f3308c1c))


### Features

* **backend:** add api endpoint to get feedback stats ([bb2110d](https://github.com/jmiguelv/iREAL/commit/bb2110d581cddc6f144d289dfd2a09994cd6cfd7))
* **frontend:** add link from about to the chat ([6cd119a](https://github.com/jmiguelv/iREAL/commit/6cd119aa65be29eea50aeb718bb9f2de7682234c))
* **frontend:** add section to display feedback stats ([61c751d](https://github.com/jmiguelv/iREAL/commit/61c751dfb285d0c39107d773d16f1da50054a304))
* **frontend:** reduce the size of the example questions buttons ([000b834](https://github.com/jmiguelv/iREAL/commit/000b834ffec7b47fa811dcba5a20dcf10e9761c5))
* **frontend:** reduce the size of the feedback and action buttons for each answer ([54a1e51](https://github.com/jmiguelv/iREAL/commit/54a1e51d8b2afdc388fd96145e58940fd5138b4f))

# [0.5.0](https://github.com/jmiguelv/iREAL/compare/v0.4.0...v0.5.0) (2024-10-01)


### Bug Fixes

* **api:** add cors middleware ([99427de](https://github.com/jmiguelv/iREAL/commit/99427ded15ae442d229857d4d139d1013dc5f4ae))
* **backend:** change the phoenix endpoint to include only the host and port ([769ddd1](https://github.com/jmiguelv/iREAL/commit/769ddd161d9b4d732fd900a66375a09e3db2c550))
* **chat:** typo ([59504ee](https://github.com/jmiguelv/iREAL/commit/59504ee28534e64a2e6bd56d8ccadd18668375af))
* **chat:** typo ([c370492](https://github.com/jmiguelv/iREAL/commit/c3704923761bd7a3d1bf3303b6e12ef2254dd263))
* **cli:** restore the prompt for the retriever query engine ([5a9b017](https://github.com/jmiguelv/iREAL/commit/5a9b0176a5a6293ca7b0b08a23a2c8ffc467ad13))
* **frontend:** change the api endpoint to make it more generic ([79c43e9](https://github.com/jmiguelv/iREAL/commit/79c43e96b387ff4ecbcd2ac3c971f261d91bb541))
* **frontend:** ensure the submit is handled correctly ([006a924](https://github.com/jmiguelv/iREAL/commit/006a9247966a336e350bcede5983050d2aca799a))
* **frontend:** remove debug logging ([5859e23](https://github.com/jmiguelv/iREAL/commit/5859e23dd5ab01a362b4a5978d272c7d87e6231b))
* **frontend:** typo ([7b4bcdb](https://github.com/jmiguelv/iREAL/commit/7b4bcdbaf785ec7e545b45ec9a3f4111262fae01))


### Features

* **api:** add endpoint to collect feedback ([6f89792](https://github.com/jmiguelv/iREAL/commit/6f89792e17752938d61d94092c54581fabb159e7))
* **api:** add workers to uvicorn ([75e2331](https://github.com/jmiguelv/iREAL/commit/75e23315e5611c3cff8f23bf118467ae577129ef))
* **backend:** add api for rag ([8b3beea](https://github.com/jmiguelv/iREAL/commit/8b3beea3c86bb373b7316f33d72dc86a6bcdf789))
* **backend:** add trace information to the query responses ([6dee721](https://github.com/jmiguelv/iREAL/commit/6dee721968b5f0a750d9d6b8f3f2a6252a8423ad))
* **chat:** add a marker for retried questions ([c89d975](https://github.com/jmiguelv/iREAL/commit/c89d9757b81f34f24cd8e2b805d1a198c0df9c04))
* **chat:** add help section ([511a511](https://github.com/jmiguelv/iREAL/commit/511a511d3160256a64ef937876ec695907fbb00c))
* **chat:** display the default prompt in the customise section ([9186fb1](https://github.com/jmiguelv/iREAL/commit/9186fb1de6701741d5c686665175400db2cf730b))
* **chat:** expand the description of the example questions ([77a9030](https://github.com/jmiguelv/iREAL/commit/77a9030b3095ecc9012200d438f1589d573bc3d7))
* **chat:** expand the explanation about the chatbot ([5836b31](https://github.com/jmiguelv/iREAL/commit/5836b31b96b770a4a99c6e939b93d2bce3defd1f))
* **frontend:** add functionality to collect user feedback on the answers ([ae239e9](https://github.com/jmiguelv/iREAL/commit/ae239e9a471abf380570cda95c3993ae6c8935b9))

# [0.4.0](https://github.com/jmiguelv/iREAL/compare/v0.3.0...v0.4.0) (2024-09-24)


### Bug Fixes

* **backend:** add prompt to the retriever query engine ([234af2e](https://github.com/jmiguelv/iREAL/commit/234af2e5c8d8c12c193b84528d3263db462e6756))
* **frontend:** use data preparation instead of pre-processing ([3aec3bb](https://github.com/jmiguelv/iREAL/commit/3aec3bbf17a6051de4d71bbf825d93e0bc0d2a4f))


### Features

* **backend:** enable observability ([ff4c14f](https://github.com/jmiguelv/iREAL/commit/ff4c14f56876f69f7e4eac475ab5e40cafd1bd61))
* **frontend:** add contact details ([b58760e](https://github.com/jmiguelv/iREAL/commit/b58760efb7be7f9aa6e9f1c66d0ea99570f110c6))
* **frontend:** add llm prompts ([ee56c55](https://github.com/jmiguelv/iREAL/commit/ee56c55163a76746a4656fb92e7a7bee52ba20c0))
* **frontend:** expand the ethics section ([ac94052](https://github.com/jmiguelv/iREAL/commit/ac9405288310d88052126f1194c3b5fce5656c9a))
* **frontend:** expand the explanation about the map view ([ca7a312](https://github.com/jmiguelv/iREAL/commit/ca7a31225823333cda76d90b81cba83ac7e90461))

# [0.3.0](https://github.com/jmiguelv/iREAL/compare/v0.2.2...v0.3.0) (2024-09-10)


### Bug Fixes

* **frontend:** exclude diseases and years from the entities ([2e8931f](https://github.com/jmiguelv/iREAL/commit/2e8931f3467b9acb27e39d79ce5304bcf729962d))
* **frontend:** remove duplicate column from the table ([7067aae](https://github.com/jmiguelv/iREAL/commit/7067aae1b3d8061f5138e05248c307f00f06be4a))


### Features

* **frontend:** add about page ([4c0e4c2](https://github.com/jmiguelv/iREAL/commit/4c0e4c28c475fa8d0a009dddb79608833acad5bf))
* **frontend:** add latest version of the data ([15106fb](https://github.com/jmiguelv/iREAL/commit/15106fbb3a88c43a6465b506f15955a791000ed3))

## [0.2.2](https://github.com/jmiguelv/iREAL/compare/v0.2.1...v0.2.2) (2024-09-03)


### Bug Fixes

* **frontend:** remove log statement ([4810551](https://github.com/jmiguelv/iREAL/commit/481055188f134bc7f66d3e15a979d9fd784987ab))


### Features

* **frontend:** add favicon ([8224c47](https://github.com/jmiguelv/iREAL/commit/8224c479361d3f77cee5dc44917f25438779bbde))

## [0.2.1](https://github.com/jmiguelv/iREAL/compare/v0.2.0...v0.2.1) (2024-09-03)


### Bug Fixes

* **frontend:** remove debug information ([f8e7879](https://github.com/jmiguelv/iREAL/commit/f8e7879f9ea75837804c479cd9d52df113982ee5))

# [0.2.0](https://github.com/jmiguelv/iREAL/compare/v0.1.0...v0.2.0) (2024-09-03)


### Features

* **backend:** add step in the indexing pipeline to extract years ([4198971](https://github.com/jmiguelv/iREAL/commit/41989716884b97c0e6829358c0d70d7f17e6b749))
* **frontend:** add pre-defined list of topics ([e148c0c](https://github.com/jmiguelv/iREAL/commit/e148c0ce2e0a428f8c47461854dbff853a2a1cda))
* **frontend:** add years to the list of entity fields ([edfeea0](https://github.com/jmiguelv/iREAL/commit/edfeea0fb52cee1f87cddde8e898b07771bc4817))
* **frontend:** cleanup the extracted data ([939a8c4](https://github.com/jmiguelv/iREAL/commit/939a8c487043c504c80de580241c423b595a7926))
* **frontend:** display and highlight years ([ece9128](https://github.com/jmiguelv/iREAL/commit/ece91281813dd8b8a7f5e4c5364c7e2d93592267))
* **frontend:** display year span using the extracted years ([30a4ce8](https://github.com/jmiguelv/iREAL/commit/30a4ce842de04fd1a97b9e15fade2c14f64bba41))
* **transformers:** add transformer to extract years from nodes ([760c120](https://github.com/jmiguelv/iREAL/commit/760c120269cc468b1bd24b1c1ef3b826531deb83))


### Performance Improvements

* **frontend:** use the pre-extracted entities for the school ([25eb426](https://github.com/jmiguelv/iREAL/commit/25eb42697cf78452a97a89db3a5fdb08391d82de))

# 0.1.0 (2024-08-30)


### Bug Fixes

* **facetdistribution:** set min count comparision to be >= ([91c4b70](https://github.com/jmiguelv/iREAL/commit/91c4b705918db687365576e5e1d113f02e1ef81f))
* **facetdistribution:** sort filters by name ([a2ac652](https://github.com/jmiguelv/iREAL/commit/a2ac6524a03bcdc9d1af45ebd7c04d37fce12d5d))
* **facetmap:** add aria role to markers ([11df788](https://github.com/jmiguelv/iREAL/commit/11df7888bbb81c7ebed5319b046dcaf128a2230c))
* **facetmap:** remove log statement ([31d9f0f](https://github.com/jmiguelv/iREAL/commit/31d9f0f92063c9f6faf78f04a1d8df20164b7894))
* **frontend:** add class to prevent style conflicts ([251b801](https://github.com/jmiguelv/iREAL/commit/251b80132258fadb83018dc0dc5454164cbdac63))
* **frontend:** align row count with pagination ([8119aaf](https://github.com/jmiguelv/iREAL/commit/8119aaf2c16f76f0c11bf4c744e8499bd04c9958))
* **frontend:** remove getEntries function ([26b0fad](https://github.com/jmiguelv/iREAL/commit/26b0fad808fabddefa5b3b99e4d7b930c06650fe))
* **frontend:** remove unused imports ([29ef07e](https://github.com/jmiguelv/iREAL/commit/29ef07eb0261510e70231c416bef979b58a87f31))
* **frontend:** typo ([698b639](https://github.com/jmiguelv/iREAL/commit/698b6397d7cdc6e03b68bf98dfd42bd4491737b4))
* **frontend:** typo ([d0e207a](https://github.com/jmiguelv/iREAL/commit/d0e207af766535892b90f97f8e47fcf406b282d0))
* **frontend:** update headers ([a1acbf5](https://github.com/jmiguelv/iREAL/commit/a1acbf54a58d6bf71c15a71f5df30acc7e5fea17))
* **themetoggle:** replace link with button for better accessibility ([3b36771](https://github.com/jmiguelv/iREAL/commit/3b367717bde2910774a794de983bb2eb98a41f00))
* **themetoggle:** use prefers-color-scheme to match window theme ([6f04fd8](https://github.com/jmiguelv/iREAL/commit/6f04fd84bb2521157388023a392edf820fee05cd))


### Features

* **backend:** add backend app ([db77b08](https://github.com/jmiguelv/iREAL/commit/db77b082a0c02e8b463d3af3992158c8901e9b67))
* **backend:** add bm25 retriever for hybrid search and cache support ([24d3f08](https://github.com/jmiguelv/iREAL/commit/24d3f08e210ceef0c15b52322fa42c699dfd1536))
* **backend:** add topic extractor and geocode transformer ([e17a26b](https://github.com/jmiguelv/iREAL/commit/e17a26b998e4367d0856e30ffd95c5f084fb2c54))
* **facetdistribution:** add option to filter the facet ([cf857b7](https://github.com/jmiguelv/iREAL/commit/cf857b74fdb25eb334ea5e42fe1758cb09184528))
* **facetdistribution:** add simple filter by facet ([1920769](https://github.com/jmiguelv/iREAL/commit/1920769431f57622c72acddb236f7b3641fec510))
* **facetdistribution:** add switch to sort by label/count ([dbfaeca](https://github.com/jmiguelv/iREAL/commit/dbfaeca222b612eb9b24a3948fd2eba51694feaf))
* **facetdistribution:** set the charts font ([0591dac](https://github.com/jmiguelv/iREAL/commit/0591dac3b85a9d97d5a964ea79c9dc83b642e4e8))
* **facetdistribution:** when filtering display also display co-occurring facets ([b630501](https://github.com/jmiguelv/iREAL/commit/b630501bc53562eb4256d2c2fe0fff093c77aded))
* **facetmap:** increase the map height ([216a6d4](https://github.com/jmiguelv/iREAL/commit/216a6d4f509592568d89259fea42d478b472bc67))
* **facetmap:** increase zoom to 5 ([96fdd49](https://github.com/jmiguelv/iREAL/commit/96fdd4933d37ae77ff9b14f0d2ccda41673a1001))
* **frontend:** add a mark when in dev mode ([3819ab7](https://github.com/jmiguelv/iREAL/commit/3819ab70952c8a6784a8bbc16876f56481420fe4))
* **frontend:** add component to render internal links ([8dc7694](https://github.com/jmiguelv/iREAL/commit/8dc76940481b93d489d4e242c594d780d6053792))
* **frontend:** add component to toggle colour theme ([2b2406b](https://github.com/jmiguelv/iREAL/commit/2b2406b6a250b59f74ca91d1ea358af4da5e5410))
* **frontend:** add initial implementation of dashboard ([6f70b07](https://github.com/jmiguelv/iREAL/commit/6f70b07b594e6ec02309a52808b4587dfe70f6a3))
* **frontend:** add link from overview to organisations ([18a4694](https://github.com/jmiguelv/iREAL/commit/18a46945bd7b02a0f853a457626b6af15fbd8923))
* **frontend:** add link to github repository ([a45cf61](https://github.com/jmiguelv/iREAL/commit/a45cf615c1e7961bc1180a848d562859aff66a4a))
* **frontend:** add main css ([4b5e99e](https://github.com/jmiguelv/iREAL/commit/4b5e99eb899a3a6bbec78dd792430292d890334e))
* **frontend:** add map visualisation ([cd89d6c](https://github.com/jmiguelv/iREAL/commit/cd89d6c5ceb233dd533754181f5aacda3ce3d601))
* **frontend:** add option to highlight entities in the school records ([e788d67](https://github.com/jmiguelv/iREAL/commit/e788d672d870986bc9618f4c72786605346392c8))
* **frontend:** add route to render the school records ([2b2e390](https://github.com/jmiguelv/iREAL/commit/2b2e39021b7ebbbe3a22c2ae4fd43d222b0b2e16))
* **frontend:** add view to display organisations ([327d5ff](https://github.com/jmiguelv/iREAL/commit/327d5ff4cb5b891f838349969c0bfe7452b65e8d))
* **frontend:** add view to display the processed data for a school ([7325ca0](https://github.com/jmiguelv/iREAL/commit/7325ca0c094997b41852c1f29b58a6b1e8c13724))
* **frontend:** always display the dashboard intro section ([b046e61](https://github.com/jmiguelv/iREAL/commit/b046e61099c1dd48df29ffd1fce8fce2c2b97c3e))
* **frontend:** define font family var ([18c40d7](https://github.com/jmiguelv/iREAL/commit/18c40d70bd4a76affcd0f8d8b3d31872b4fa9a75))
* **frontend:** display places in the schools table ([c138475](https://github.com/jmiguelv/iREAL/commit/c138475978b451f4035e91ba643c2a7af9d85776))
* **frontend:** display the version in the dashboard ([3f7ab4f](https://github.com/jmiguelv/iREAL/commit/3f7ab4f2efa28e95d5b9b294b3e388a1e28fe4cd))
* **frontend:** highlight keywords in the school record ([dc6e12f](https://github.com/jmiguelv/iREAL/commit/dc6e12feb8018f605ac6602daef507f664a9239d))
* **frontend:** reduce the min count for keywords and topics to 1 ([fc40c40](https://github.com/jmiguelv/iREAL/commit/fc40c40c2404f8049582f4a83e6660235ad8424e))
* **schools:** highlight entities in the school record ([5ee5d28](https://github.com/jmiguelv/iREAL/commit/5ee5d288b22a776c3fa9552db57ccd8380d45a66))
