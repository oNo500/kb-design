---
id: decision-term-data-values
schema: urn:kb-design:data:decision
schema_version: 1
status: accepted
date: '2026-09-06'
level: L3
scope: 全量术语具体值、名称地位与明确旧名处置；不授予publication
supersedes: []
answers:
- question: Q01
  resolution: recommended
  patches:
  - identity: terms/concepts/tc-6908a022-5a5a-43e0-b895-4414bba97169
    field: record
    value:
      id: tc-6908a022-5a5a-43e0-b895-4414bba97169
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 预先规定的词、标目（headings）或代码列表，每项表示一个概念。
        basis:
        - entity: iso-25964-1
          locator: §2.12；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-67cf1d57-71a5-4e5a-8294-ca5d0a931222
          text: controlled vocabulary
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.12；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-e92e1633-a6e8-4eaa-91cd-fc1abd2d7cd3
          text: 受控词表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 受控词表是信息组织领域对预定且受管理的词汇列表的通行表达；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.12；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-c960c1a6-3e65-4075-801a-876b1d3b2f57
    field: record
    value:
      id: tc-c960c1a6-3e65-4075-801a-876b1d3b2f57
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 思维单元；独立于表达它的词而存在。
        basis:
        - entity: iso-25964-1
          locator: §2.11；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-0cad325d-695d-4f83-a05a-9ba8cb422e8a
          text: concept
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.11；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-1c54182a-deb7-427a-8426-68bd35811502
          text: 概念
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 概念对应思维单元而非字符串，是术语学与知识组织的基本表达；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.11；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-c1473abd-3fc6-4570-bf19-cbb27b944fc2
    field: record
    value:
      id: tc-c1473abd-3fc6-4570-bf19-cbb27b944fc2
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 标引时用来表示概念的词。
        basis:
        - entity: iso-25964-1
          locator: §2.45；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-6819b288-3cb6-4479-9516-e2a25acf1618
          text: preferred term
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.45；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
        - id: tm-b13a05dd-249c-4d95-b82d-d575249ffd1f
          text: descriptor
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.45 preferred term / descriptor；免费样章印刷p.9，本次直接重读
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-d7a0c93f-489a-4385-93ce-a934df56a82f
          text: 首选词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 首选词突出标引时优先采用的名称；旧并列叙词暂不凭逗号加入同义形式；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
        - id: tm-b662786b-e53c-4ed0-9cc8-35346e4c6e20
          text: 叙词
          administrative_status: admittedTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 叙词是图书情报与叙词表实践中descriptor的既有中文名称；本条限定标引时代表概念的首选词，不泛指任意词；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.45；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-75fa8baa-d6ec-400e-b90f-5039371a2d57
    field: record
    value:
      id: tc-75fa8baa-d6ec-400e-b90f-5039371a2d57
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 不分配给文档、但作为叙词表或索引入口的词。
        basis:
        - entity: iso-25964-1
          locator: §2.39；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-1996dfd0-ddc6-437f-808f-5ad8ff4f2b81
          text: non-preferred term
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.39；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-cd530576-f163-4651-b468-3dbf8af5f014
          text: 非首选词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 非首选词与首选词形成名称使用地位的对照；非叙词保留原登记待独立判断；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
        - id: tm-3866b74f-a77b-46e9-95bc-f4b16fefd182
          text: 非叙词
          administrative_status: admittedTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 非叙词对应ISO§2.39同时列出的non-descriptor，在此指不用作直接标引而提供入口的词；与非首选词同范围；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.39；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-dc59744d-a530-44b7-9de8-77e2766710e7
    field: record
    value:
      id: tc-dc59744d-a530-44b7-9de8-77e2766710e7
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在确定的语境或资源内，为唯一识别概念、词或其他实体而使用的一组符号。
        basis:
        - entity: iso-25964-1
          locator: §2.25；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-de3b29f2-97c9-489a-be7a-0c77c1368e29
          text: identifier
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.25；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-a596d0b5-6739-41d4-a914-5171aa299fb5
          text: 标识符
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 标识符用于识别对象而非描述对象，译名保留识别语义；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.25；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-75e8012c-351f-4303-b8c0-523454b9b730
    field: record
    value:
      id: tc-75e8012c-351f-4303-b8c0-523454b9b730
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 叙词表中两个词表示同一个概念的关系。
        basis:
        - entity: iso-25964-1
          locator: §2.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: zh-Hans
        terms:
        - id: tm-1192a98f-d6b3-44ee-a68f-d2c60cad8464
          text: 等价关系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 等价关系在此连接两个表示形式，不混作跨词表映射；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-278494cf-719c-43f9-b954-2a54c61e5c45
    field: record
    value:
      id: tc-278494cf-719c-43f9-b954-2a54c61e5c45
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 两个概念之间，一个概念的范围完全包含在另一个概念范围内的关系。
        basis:
        - entity: iso-25964-1
          locator: §2.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: zh-Hans
        terms:
        - id: tm-649ce784-1d46-4f8a-8d77-b093d37b085a
          text: 层级关系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 层级关系表示范围包含，保留与等价和相关关系的区别；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-589f6145-5330-4773-b2dd-27eeeaa6bc84
    field: record
    value:
      id: tc-589f6145-5330-4773-b2dd-27eeeaa6bc84
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 两个概念没有层级关系，但具有强语义联系的关系。
        basis:
        - entity: iso-25964-1
          locator: §2.2；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: zh-Hans
        terms:
        - id: tm-97b3a73e-ff28-43f8-a01a-be24595a7b24
          text: 相关关系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 相关关系是叙词表中非层级的语义关联；RT 保留为关系符号；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.2；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-1fa87658-bf07-4540-a863-a4e98a2fa888
    field: record
    value:
      id: tc-1fa87658-bf07-4540-a863-a4e98a2fa888
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 属于同一固有类别的概念分组。
        basis:
        - entity: iso-25964-1
          locator: §2.20；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-960f6e22-a8fe-426c-b6ea-7f92f697d188
          text: facet
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.20；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-7dbccdb3-ab81-4d56-95cc-7b55b1e3d83a
          text: 分面
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 分面是分面分类法对共同固有类别分组的传统译名；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.20；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-99e3245e-2f51-45d0-ba40-800d645f7f1f
    field: record
    value:
      id: tc-99e3245e-2f51-45d0-ba40-800d645f7f1f
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 把主题领域分析为概念，按分面分组，并按划分特征细分概念。
        basis:
        - entity: iso-25964-1
          locator: §2.21；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-b60105ff-8590-4f3e-82dd-41b3e6f9d933
          text: facet analysis
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.21；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-31f1451a-6a7e-4415-b0e4-02c445d722c9
          text: 分面分析
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 分面分析表示上述分析和分组方法，不是给文档加多个字段；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.21；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-a5b2fb0f-5cea-4d47-8629-04694918cbf9
    field: record
    value:
      id: tc-a5b2fb0f-5cea-4d47-8629-04694918cbf9
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用来把一个概念细分为一组下位概念的属性；组内各概念具有该属性的不同值。
        basis:
        - entity: iso-25964-1
          locator: §2.4；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-e992d008-5b21-4068-891d-6a4bbd30561d
          text: characteristic of division
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.4；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-58a4412c-5306-4b39-99dc-ab139550b589
          text: 划分特征
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 划分特征突出同级细分所依据的属性，避免把属性值本身叫特征；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.4；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-6e6f7a15-910d-483e-b06c-3e3938aed39b
    field: record
    value:
      id: tc-6e6f7a15-910d-483e-b06c-3e3938aed39b
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 插入层级或分类显示、说明词如何安排的标签；它既不是首选词，也不是非首选词。
        basis:
        - entity: iso-25964-1
          locator: §2.38；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-cf8405c5-923a-4e3c-9ebc-fd08013905af
          text: node label
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.38；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-3e5b4977-db0a-413a-8556-f8f4b34fd5bc
          text: 节点标签
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 节点标签在词表显示中说明排列，不是普通图节点的名称；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.38；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-c09e918a-cc3f-423c-bbca-c40c6766ef28
    field: record
    value:
      id: tc-c09e918a-cc3f-423c-bbca-c40c6766ef28
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 一组兄弟概念。
        basis:
        - entity: iso-25964-1
          locator: §2.1；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-d8924442-07c0-4937-b3d3-3b198a24d8aa
          text: array
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.1；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-70716b70-18a1-43d7-829a-1f174ebfc953
          text: 数组
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 数组在此限于叙词表的一组兄弟概念，与程序存储数组同形但不同义；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.1；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-6ce2328c-e952-40b8-b7d5-fd8dd958d0b7
    field: record
    value:
      id: tc-6ce2328c-e952-40b8-b7d5-fd8dd958d0b7
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 按指定准则选择的一组概念。
        basis:
        - entity: iso-25964-2
          locator: §3.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-83940a42-c171-42dd-b8db-84d62d19f2c6
          text: concept group
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-96cb412b-bb9d-4f29-93f4-4e1b9bac16c3
          text: 概念组
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 概念组直指按准则选出的概念集合；过宽的分组暂保留原登记；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
        - id: tm-5627bc80-145c-48a0-ba62-f54c7ac3b83c
          text: 分组
          administrative_status: admittedTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 分组在中文可指动作或结果；本条严格指按准则选定的概念集合，作为概念组的简短称呼，不表示分组操作或任意数据集合；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-c47ee168-3ad4-4489-bc26-1cc64f94407f
    field: record
    value:
      id: tc-c47ee168-3ad4-4489-bc26-1cc64f94407f
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用于一致命名特定实体的受控词表；这些实体是唯一的个体而非类。
        basis:
        - entity: iso-25964-2
          locator: §3.50；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-6936dadd-bd45-487a-b3e1-0ec61a2f7c64
          text: name authority list
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.50；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-a92be9a9-8e86-4aac-931c-4a5072bb461a
          text: 名称规范表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 名称规范表是规范控制中对个体名称保持一致的名称列表表达；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.50；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-405390d9-57dc-47ca-9317-0120d5aa86eb
    field: record
    value:
      id: tc-405390d9-57dc-47ca-9317-0120d5aa86eb
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 说明目标词表中的概念与源词表中的概念在范围上被视为相同的映射。
        basis:
        - entity: iso-25964-2
          locator: §3.27；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-a570aee4-b8a3-4fa4-a3a4-1d40403444dc
          text: equivalence mapping
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.27；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-7d69db17-67ab-436d-9994-539c6702b0e0
          text: 等价映射
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 等价映射限定跨词表的概念对应，与表内词的等价关系区分；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.27；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-eb9e1973-6b39-47f1-8b3e-845798b14ba4
    field: record
    value:
      id: tc-eb9e1973-6b39-47f1-8b3e-845798b14ba4
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 旨在区分映射不同类型和质量的方法。
        basis:
        - entity: iso-25964-2
          locator: §3.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-63f76467-9cba-462a-bf20-40fa3ef63225
          text: differentiated mapping
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-8812567a-6b12-4d95-a87c-363250e59b95
          text: 区分式映射
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 区分式映射表达区分映射类型与质量的既有中文名称，不引入新的程度类别；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-b544dcf4-e88e-4456-bb9e-824b74d7abc8
    field: record
    value:
      id: tc-b544dcf4-e88e-4456-bb9e-824b74d7abc8
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 映射过程的产物，即一个词表中的一个概念与另一个词表中一个或多个概念之间的关系。
        basis:
        - entity: iso-25964-2
          locator: §3.41；docs/references/iso-25964.md 已核定义表
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-180f1491-60d9-4ad6-ba75-1ba53e68fc61
          text: mapping
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.41；docs/references/iso-25964.md 已核定义表
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-9be97554-ada5-484d-848e-8d07cda553e1
          text: 映射
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 映射是信息组织中表示不同词表概念对应关系的既有中文表达；本行严格限于 §3.41 关系产物，不引入过程义。外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.41；docs/references/iso-25964.md 已核定义表
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-c5f2ed53-7f7e-40a1-8c89-a07dac98107b
    field: record
    value:
      id: tc-c5f2ed53-7f7e-40a1-8c89-a07dac98107b
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 一组检索时视为等价的词；只用于检索，不用于标引
        basis:
        - entity: z39-19
          locator: §5.4.2；PDF page index 28-29
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-28740536-c0a9-499e-b167-e47449e37cff
          text: synonym ring
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §5.4.2；PDF page index 28-29
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-fc11144d-35cd-472b-a85d-23bc72f9e6c2
          text: 同义词环
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 同义词环指检索时视为等价的一组词，名称突出检索扩展而非标引选词；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §5.4.2；PDF page index 28-29
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-c6190e59-1353-4f22-8a93-b3077b486884
    field: record
    value:
      id: tc-c6190e59-1353-4f22-8a93-b3077b486884
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 全部由首选词构成、以层级或多层级连接的受控词表
        basis:
        - entity: z39-19
          locator: §5.4.3；PDF page index 29
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-3fbb53ad-04df-4f9d-b94f-58cecc7d80b8
          text: taxonomy
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §5.4.3；PDF page index 29
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-fc044200-56a9-4783-b4df-a6c1fc3f51e4
          text: 分类法
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 分类法是知识组织中 taxonomy 的既有行业译名；此处限于首选词的层级受控词表；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §5.4.3；PDF page index 29
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-5c7a2951-c99c-4597-baa5-c6eb7fd7c5e4
    field: record
    value:
      id: tc-5c7a2951-c99c-4597-baa5-c6eb7fd7c5e4
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 按已知顺序排列、用标准化关系指示符清楚显示词间关系的受控词表
        basis:
        - entity: z39-19
          locator: §5.4.4；PDF page index 29
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-baf0b11a-4d8a-415b-83d9-0f6d64662d6a
          text: thesaurus
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §5.4.4；PDF page index 29
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-8b27bf95-89c5-4e8b-a033-e0defb04a51c
          text: 叙词表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 叙词表是信息检索领域对具有规范关系的受控词表的传统名称；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §5.4.4；PDF page index 29
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-26a41c49-f435-4527-b419-de688657db90
    field: record
    value:
      id: tc-26a41c49-f435-4527-b419-de688657db90
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 加在词后区分同形异义的定义性词，如 `Apple (company)`
        basis:
        - entity: z39-19
          locator: §4.1；§6.2.1；PDF page index 19；31-32
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-d9b07ebb-8bba-4a1b-8b14-350fda733371
          text: qualifier
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §4.1；§6.2.1；PDF page index 19；31-32
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-d3e0ce32-0761-40d2-b0ca-4bf9dbf7a110
          text: 限定词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 限定词用于限制名称解释范围并区分同形异义；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §4.1；§6.2.1；PDF page index 19；31-32
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-7f29a362-cc5b-481a-87df-67ff11c9c068
    field: record
    value:
      id: tc-7f29a362-cc5b-481a-87df-67ff11c9c068
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 可被组织或分类以供检索的项目，包括文档、图像、人、组织和实物；本条限于 NISO 内容对象语境。
        basis:
        - entity: z39-19
          locator: §4.1；§5.2.2；PDF page index 15；22-23
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-2b91ad37-5e29-4f00-90f7-6fc791205905
          text: content object
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §4.1；§5.2.2；PDF page index 15；22-23
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-26d027c7-af05-417b-a6b5-6c1523e04613
          text: 内容对象
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 内容对象表明被组织和检索的对象，不自动等同本库内容单元；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §4.1；§5.2.2；PDF page index 15；22-23
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-74b2becc-3bbe-45b5-8d42-bda67dcc17f8
    field: record
    value:
      id: tc-74b2becc-3bbe-45b5-8d42-bda67dcc17f8
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 说明词的覆盖范围和用法限制的注释
        basis:
        - entity: z39-19
          locator: §4.1；§6.2.2；PDF page index 20；33
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-00cb8d21-abc0-4676-8a07-bafda70bd0cb
          text: scope note
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §4.1；§6.2.2；PDF page index 20；33
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-a1591f11-abf4-440c-865b-2b448311b1c3
          text: 范围注释
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 范围注释说明名称采用的含义与使用边界；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §4.1；§6.2.2；PDF page index 20；33
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-e7c36840-9dc5-45d1-a371-920c28af2a00
    field: record
    value:
      id: tc-e7c36840-9dc5-45d1-a371-920c28af2a00
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 入表日期、变更记录、旧形式及有效期
        basis:
        - entity: z39-19
          locator: §4.1；§6.2.3；§11.3.2.2；PDF page index 19；33-34；108
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-d6b7cf59-38bf-4400-a676-04b7e516cdc1
          text: history note
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §4.1；§6.2.3；§11.3.2.2；PDF page index 19；33-34；108
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-d1bad412-4998-412f-9e3a-0fdf3c1e3740
          text: 历史注释
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 历史注释记录术语的时间变化，与说明概念含义的范围注释区别；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §4.1；§6.2.3；§11.3.2.2；PDF page index 19；33-34；108
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-155c651f-9cb6-4e89-b394-9b843b268148
    field: record
    value:
      id: tc-155c651f-9cb6-4e89-b394-9b843b268148
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 提出但未走完审批的词
        basis:
        - entity: z39-19
          locator: §4.1；§11.1.6；PDF page index 19；104
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-8ec912e8-3242-45f7-bf32-97bd40f61efe
          text: candidate term
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §4.1；§11.1.6；PDF page index 19；104
            checked: '2026-09-06'
        - id: tm-e995203f-bdd8-4c79-8368-d199e049c0d2
          text: provisional term
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §4.1；§11.1.6；PDF page index 19；104
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-e7b7cd31-246e-4986-b5d3-d2fa7cb059b0
          text: 候选词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 候选词表示尚未完成收录审批的名称，而非来源实体状态；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §4.1；§11.1.6；PDF page index 19；104
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-a17e54a7-07e9-459e-86cc-bd0c12e4d58b
    field: record
    value:
      id: tc-a17e54a7-07e9-459e-86cc-bd0c12e4d58b
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 为补全层级而收、尚未用于标引的词
        basis:
        - entity: z39-19
          locator: §11.1.8；PDF page index 104
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-3f9dbaa9-c7b6-40d6-b4d1-8c83221df19b
          text: unassigned term
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §11.1.8；PDF page index 104
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-3d5a2c5e-8990-4a32-9a37-6a6b18d8f1e9
          text: 未标引词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 未标引词强调尚未实际分配给内容对象，不表示禁止使用；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §11.1.8；PDF page index 104
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-88088c7a-5aaf-458c-a55c-23ff38463ee0
    field: record
    value:
      id: tc-88088c7a-5aaf-458c-a55c-23ff38463ee0
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 没有任何层级或相关关系的词
        basis:
        - entity: z39-19
          locator: §4.1；§11.4.4；PDF page index 19；112
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-4311cc75-0005-46aa-a296-0c6c9aa89900
          text: orphan term
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §4.1；§11.4.4；PDF page index 19；112
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-d6b4f6d9-8e3f-4d8c-b418-79688e2cc5df
          text: 孤儿词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 孤儿词是缺乏层级和相关联系的词表维护用语；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §4.1；§11.4.4；PDF page index 19；112
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-6cb09f56-afea-40d2-a986-c0d80d376363
    field: record
    value:
      id: tc-6cb09f56-afea-40d2-a986-c0d80d376363
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 词是领域文献里实际通行的说法
        basis:
        - entity: z39-19
          locator: §5.3.5.1；PDF page index 27
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-2bcd97cb-cdf8-4d28-b8ab-7e688f8d1d7e
          text: literary warrant
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §5.3.5.1；PDF page index 27
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-dfed1194-5cd6-48d1-8667-a5c47ebb30bb
          text: 文献依据
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 文献依据以领域文献中的实际使用作为收词理由；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §5.3.5.1；PDF page index 27
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-1ad36b83-83d4-4174-8cc0-a6189b8ce11b
    field: record
    value:
      id: tc-1ad36b83-83d4-4174-8cc0-a6189b8ce11b
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 词是使用组织偏好的形式
        basis:
        - entity: z39-19
          locator: §5.3.5.2；PDF page index 27
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-7046ee19-1db6-4df4-9664-aa85f07387fb
          text: organizational warrant
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §5.3.5.2；PDF page index 27
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-b7475d7a-e888-4f21-ac57-b1801222311e
          text: 组织依据
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 组织依据突出采用组织偏好的名称形式；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §5.3.5.2；PDF page index 27
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-60cd4ded-814a-46d1-9bd6-360f1b725ca0
    field: record
    value:
      id: tc-60cd4ded-814a-46d1-9bd6-360f1b725ca0
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 词是用户检索时实际用的说法
        basis:
        - entity: z39-19
          locator: §5.3.5.3；PDF page index 27
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-e4155133-bdc6-4af2-9231-29ac5963363d
          text: user warrant
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §5.3.5.3；PDF page index 27
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-dcdba69e-639f-4ce6-b2ab-bea261846a7f
          text: 用户依据
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 用户依据反映检索用户实际使用的表达；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §5.3.5.3；PDF page index 27
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-60ca56e9-0bf5-4e06-86c4-b6941a9adc6e
    field: record
    value:
      id: tc-60ca56e9-0bf5-4e06-86c4-b6941a9adc6e
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 通过控制同义词、区分同形异义词并建立词间关系，使标引者和检索者能够一致表达概念的过程。
        basis:
        - entity: z39-19
          locator: §1.2；§4.1；PDF page index 12；21
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-1492b91e-ee09-46b6-b487-6d769897554e
          text: vocabulary control
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §1.2；§4.1；PDF page index 12；21
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-614c6eb9-c481-41b5-8374-d4be3d62b4d5
          text: 词汇控制
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 词汇控制是协调同义、异义和关系以使标引检索一致的行业表达；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §1.2；§4.1；PDF page index 12；21
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63
    field: record
    value:
      id: tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 有限的一组词，按字母或其他明显逻辑排列，无关系
        basis:
        - entity: z39-19
          locator: §5.4.1；印刷 p.17
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-18e3b5c1-b6c5-4ddd-9b60-64435812ef57
          text: list
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §5.4.1；印刷 p.17
            checked: '2026-09-06'
        - id: tm-42bb0163-eaa8-4a85-9cbe-f4968c0dcd2d
          text: pick list
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §5.4.1；印刷 p.17
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-74a9e0b7-478f-48e1-9b61-00ca7b63bd12
          text: 列表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 列表是有限术语按明确顺序排列这一既有概念的行业表达；避免把glossary或code list的专门名称作为无条件同义词；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §5.4.1；印刷 p.17
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-ddf950fe-a885-4424-82f9-cfbb5d4ab330
    field: record
    value:
      id: tc-ddf950fe-a885-4424-82f9-cfbb5d4ab330
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 委员会建设词表时先识别最宽泛的词，再选择下位词达到所需具体程度，并建立层级和关系。
        basis:
        - entity: z39-19
          locator: §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-486daf92-5ede-4f80-a324-75c113c41708
          text: top down
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-713d5d4c-9326-478f-8e94-b0e5f690c812
          text: 自上而下
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 自上而下保留从宽到窄的词表建设方向；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-6f960f39-1a53-4215-932e-a89f837ac06c
    field: record
    value:
      id: tc-6f960f39-1a53-4215-932e-a89f837ac06c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 委员会建设词表时从内容对象语料得到的词开始，由范围最窄的词向更一般的词组织层级。
        basis:
        - entity: z39-19
          locator: §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-7bf170bd-f546-4f38-aa43-51e301cc2976
          text: bottom up
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-a3a9225d-75eb-41bb-b912-c8b01a442062
          text: 自下而上
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 自下而上保留从具体语料词向一般词组织的方向；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-208354ed-1338-4152-be98-ca93504c3355
    field: record
    value:
      id: tc-208354ed-1338-4152-be98-ca93504c3355
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 词表经验建设方法：先从内容对象收集足够数量的词，再由专家确定关系并从宽到窄组织层级。
        basis:
        - entity: z39-19
          locator: §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-fc3bf25c-4cd0-4393-9aca-20543b39de42
          text: deductive
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-3f18476e-cd74-4c14-a5d1-94361a9c6bc8
          text: 演绎法
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 演绎法在此是 NISO 词表建设方法的既有表达，不外推到逻辑学推理定义；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-c9b65491-09a6-4765-b208-6601af494f31
    field: record
    value:
      id: tc-c9b65491-09a6-4765-b208-6601af494f31
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 词表经验建设方法：遇到词时即选择纳入，从一开始实施词汇控制，并持续将词放入较宽类别。
        basis:
        - entity: z39-19
          locator: §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-bd7ee62c-43b5-4878-8023-dfdfc68f03d2
          text: inductive
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-31f1c425-6625-40c3-9f7d-a23b93e495fe
          text: 归纳法
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 归纳法在此突出从一开始控制和逐项组织词汇，不与普通逻辑学定义混同；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-dfe493d2-f173-4a9e-ace9-b9ffad3f0f0f
    field: record
    value:
      id: tc-dfe493d2-f173-4a9e-ace9-b9ffad3f0f0f
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 检索系统检出集合中全部相关内容对象的能力；通常以检出的相关内容对象数除以集合中全部相关内容对象数计算百分比。高查全率意味着更全面，但也可能增加检出不相关内容对象的风险。
        basis:
        - entity: z39-19
          locator: PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 947-955
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-35a8bfd4-703e-41ec-bb76-9b05e048608c
          text: recall
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 947-955
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-119ca7ee-aa9d-4d04-b352-b214e2ea3962
          text: 查全率
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 查全率是信息检索中对全部相关对象检出程度的行业名称；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 947-955
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-11e8d232-85f8-4e00-98a0-d8bdd7adf639
    field: record
    value:
      id: tc-11e8d232-85f8-4e00-98a0-d8bdd7adf639
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 检索系统只检出相关内容对象的能力；通常以检出的相关内容对象数除以检出的内容对象总数计算百分比。高查准率提高结果相关性，但可能漏掉部分相关对象。
        basis:
        - entity: z39-19
          locator: PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 918-926
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-9962ad11-5853-4ed6-aa79-43335bb9aa59
          text: precision
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 918-926
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-bd0ee821-6214-4efe-8771-67403605f612
          text: 查准率
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 查准率是信息检索中对检出结果相关程度的行业名称；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 918-926
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-9d793546-528c-4b51-8a37-801df07342f3
    field: record
    value:
      id: tc-9d793546-528c-4b51-8a37-801df07342f3
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 对概念化的明确规范，包括用于描述领域的类、属性和关系及其含义与约束。
        basis:
        - entity: gruber-official
          locator: L14-L24；英文形式 ontology；作者定义为 explicit specification of a conceptualization；代表原语包括 classes、attributes、relationships
            及其约束（L15-L16）
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-3f32ff2e-2739-4982-9971-ff06c324a402
          text: ontology
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: gruber-official
            locator: L14-L24；英文形式 ontology；作者定义为 explicit specification of a conceptualization；代表原语包括 classes、attributes、relationships
              及其约束（L15-L16）
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-f1d2d279-3d8f-4f39-b490-8f0c211d15b9
          text: 本体
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 本体是知识表示领域 ontology 的通行译名，限于概念化规范；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: gruber-official
        locator: L14-L24；英文形式 ontology；作者定义为 explicit specification of a conceptualization；代表原语包括 classes、attributes、relationships
          及其约束（L15-L16）
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-c7d6f1d5-2139-4d42-857d-7c16fa507b31
    field: record
    value:
      id: tc-c7d6f1d5-2139-4d42-857d-7c16fa507b31
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用于积累和传达现实世界知识的图数据；节点表示实体，边表示实体间关系，数据图可采用有向边标记图、属性图等模型。
        basis:
        - entity: hogan-paper
          locator: P1 L68-L89；P6 L277-L328；P1 L71-L83 直接支持现实世界知识、实体节点、实体间关系、图数据模型及可用本体/规则表达量化知识
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-2d4a0c3e-052f-4110-b3c6-9f08982cbb34
          text: knowledge graph
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hogan-paper
            locator: P1 L68-L89；P6 L277-L328；P1 L71-L83 直接支持现实世界知识、实体节点、实体间关系、图数据模型及可用本体/规则表达量化知识
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-60f284eb-71a8-490b-be2a-b6fabcb92d8b
          text: 知识图谱
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 知识图谱表述以图积累和传达知识的数据组织；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hogan-paper
        locator: P1 L68-L89；P6 L277-L328；P1 L71-L83 直接支持现实世界知识、实体节点、实体间关系、图数据模型及可用本体/规则表达量化知识
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-99ace251-fdee-4ab9-93e8-a016e7e98127
    field: record
    value:
      id: tc-99ace251-fdee-4ab9-93e8-a016e7e98127
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: DCMI 维护的元数据属性、类、数据类型和词表编码方案集合。
        basis:
        - entity: dcmi-metadata-terms
          locator: §1；DCMIType 条目；dc:type 条目；DCMI Metadata Terms 包含 properties、classes、datatypes、vocabulary encoding schemes；不是只有属性与类
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-94cd7a7d-4b17-4493-968d-12bdee0c0bb7
          text: DCMI Metadata Terms
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: dcmi-metadata-terms
            locator: §1；DCMIType 条目；dc:type 条目；DCMI Metadata Terms 包含 properties、classes、datatypes、vocabulary encoding schemes；不是只有属性与类
            checked: '2026-09-06'
      basis:
      - entity: dcmi-metadata-terms
        locator: §1；DCMIType 条目；dc:type 条目；DCMI Metadata Terms 包含 properties、classes、datatypes、vocabulary encoding schemes；不是只有属性与类
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-3f06d868-d7d2-4612-ad2b-35614912ba40
    field: record
    value:
      id: tc-3f06d868-d7d2-4612-ad2b-35614912ba40
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用于按资源性质或体裁分类的 DCMI 类集合。
        basis:
        - entity: dcmi-metadata-terms
          locator: §1；DCMIType 条目；dc:type 条目；DCMI 官方将 DCMIType 定义为用于分类资源性质或体裁的类集合；`dcterms:type` 建议使用受控词表
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-f04583f9-f962-4c1f-bf3e-8cf3748b4205
          text: DCMI Type Vocabulary
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: dcmi-metadata-terms
            locator: §1；DCMIType 条目；dc:type 条目；DCMI 官方将 DCMIType 定义为用于分类资源性质或体裁的类集合；`dcterms:type` 建议使用受控词表
            checked: '2026-09-06'
      basis:
      - entity: dcmi-metadata-terms
        locator: §1；DCMIType 条目；dc:type 条目；DCMI 官方将 DCMIType 定义为用于分类资源性质或体裁的类集合；`dcterms:type` 建议使用受控词表
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-589ad410-5fc7-4f1b-ba5a-fd06c366016f
    field: record
    value:
      id: tc-589ad410-5fc7-4f1b-ba5a-fd06c366016f
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 由主语、谓语和宾语组成的 RDF 数据单元。
        basis:
        - entity: rdf11
          locator: §3.1 Triples；RDF triple 的 subject、predicate、object 三组件；顺序为 subject-predicate-object
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-eecf3ffd-6446-4574-966d-09a7304e8a7c
          text: triple
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: rdf11
            locator: §3.1 Triples；RDF triple 的 subject、predicate、object 三组件；顺序为 subject-predicate-object
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-9fdaa528-7ee8-4a29-ae7f-a8b08aaa0380
          text: 三元组
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 三元组在 RDF 中明确对应主语、谓语、宾语三组件；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: rdf11
        locator: §3.1 Triples；RDF triple 的 subject、predicate、object 三组件；顺序为 subject-predicate-object
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-e638bec2-4c85-4eed-9721-8175f5417f6d
    field: record
    value:
      id: tc-e638bec2-4c85-4eed-9721-8175f5417f6d
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用于 RDF 数据的查询语言。
        basis:
        - entity: sparql11
          locator: §1 Introduction；SPARQL 1.1 规范定义 RDF 查询语言的 syntax 和 semantics
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-be311ab7-f917-4c29-840c-2ef0e64c23cf
          text: SPARQL
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: sparql11
            locator: §1 Introduction；SPARQL 1.1 规范定义 RDF 查询语言的 syntax 和 semantics
            checked: '2026-09-06'
      basis:
      - entity: sparql11
        locator: §1 Introduction；SPARQL 1.1 规范定义 RDF 查询语言的 syntax 和 semantics
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-acd244b6-0d82-4366-ac25-3fb7260c6473
    field: record
    value:
      id: tc-acd244b6-0d82-4366-ac25-3fb7260c6473
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用于 Web 信息表示、以主语—谓语—宾语三元组构成图的数据框架。
        basis:
        - entity: rdf11
          locator: Introduction；§3.1 Triples
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-ceea4cbc-ecb1-4aa5-9d44-82267d0d943c
          text: Resource Description Framework
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: rdf11
            locator: Introduction；§3.1 Triples
            checked: '2026-09-06'
        - id: tm-4e708f52-6a2a-4ae6-b9cb-b7286d3a85d0
          text: RDF
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: rdf11
            locator: Introduction；§3.1 Triples
            checked: '2026-09-06'
      basis:
      - entity: rdf11
        locator: Introduction；§3.1 Triples
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-2633b390-938e-4c0b-9bec-deebf8f65e8b
    field: record
    value:
      id: tc-2633b390-938e-4c0b-9bec-deebf8f65e8b
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 以 RDF 表达知识组织系统的数据模型；其 Reference 是 W3C Recommendation。
        basis:
        - entity: skos
          locator: Introduction；SKOS data model
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-7019ad5a-e9f6-4db3-8596-3e29c256455c
          text: Simple Knowledge Organization System
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: skos
            locator: Introduction；SKOS data model
            checked: '2026-09-06'
        - id: tm-e854dfc3-779a-4e51-8253-520cc3722fec
          text: SKOS
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: skos
            locator: Introduction；SKOS data model
            checked: '2026-09-06'
      basis:
      - entity: skos
        locator: Introduction；SKOS data model
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-a07a37d8-13b6-4a9d-b86c-ba96f0c080b4
    field: record
    value:
      id: tc-a07a37d8-13b6-4a9d-b86c-ba96f0c080b4
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用于 RDF 数据的数据建模词汇。
        basis:
        - entity: rdfs11
          locator: Abstract；§1
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-b710284d-ad1f-47d2-911d-616d0aba7688
          text: RDFS
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: rdfs11
            locator: Abstract；§1
            checked: '2026-09-06'
      basis:
      - entity: rdfs11
        locator: Abstract；§1
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-b4f8bca4-b3cf-405b-8cf1-ea45112783d2
    field: record
    value:
      id: tc-b4f8bca4-b3cf-405b-8cf1-ea45112783d2
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用于表达本体、具有形式语义并可与 RDF 一起使用的 Web 本体语言。
        basis:
        - entity: owl2
          locator: Abstract；§1
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-e587b46e-66cd-43a1-8423-339602565de7
          text: OWL
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: owl2
            locator: Abstract；§1
            checked: '2026-09-06'
      basis:
      - entity: owl2
        locator: Abstract；§1
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-cb8ba91f-0bce-4b3d-ac6a-26bfca9ab7c9
    field: record
    value:
      id: tc-cb8ba91f-0bce-4b3d-ac6a-26bfca9ab7c9
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 为特定应用规定 metadata term、约束、使用与编码语法的文档集合
        basis:
        - entity: dcmi-singapore-framework
          locator: §3.1–3.3；docs/references/dcmi-application-profiles.md 已核阅读范围
          checked: '2026-09-01'
      languages:
      - language: en
        terms:
        - id: tm-e35cfb69-400f-4114-925b-5b139615c090
          text: Application Profile
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: dcmi-singapore-framework
            locator: §3.1–3.3；docs/references/dcmi-application-profiles.md 已核阅读范围
            checked: '2026-09-01'
      basis:
      - entity: dcmi-singapore-framework
        locator: §3.1–3.3；docs/references/dcmi-application-profiles.md 已核阅读范围
        checked: '2026-09-01'
      workflow: active
  - identity: terms/concepts/tc-224b9f45-d624-4543-bc81-f64d02f81aa0
    field: record
    value:
      id: tc-224b9f45-d624-4543-bc81-f64d02f81aa0
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 软件产品的构建过程具有可重现性，是指在指定其源码的具体版本及全部构建依赖后，无论在哪种环境执行，每次构建都产生逐比特相同的产物。
        basis:
        - entity: lamb-zacchiroli-2021-reproducible-builds
          locator: https://arxiv.org/pdf/2104.06020v1；PDF p. 2，Reproducible Builds，Definition 1
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-849f1000-68b5-456c-954f-1b05750ebea3
          text: Reproducible Builds
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: lamb-zacchiroli-2021-reproducible-builds
            locator: https://arxiv.org/pdf/2104.06020v1；PDF p. 2，Reproducible Builds，Definition 1
            checked: '2026-09-06'
      basis:
      - entity: lamb-zacchiroli-2021-reproducible-builds
        locator: https://arxiv.org/pdf/2104.06020v1；PDF p. 2，Reproducible Builds，Definition 1
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-2cdb43fb-ad5e-4aec-ad71-56eb596b78eb
    field: record
    value:
      id: tc-2cdb43fb-ad5e-4aec-ad71-56eb596b78eb
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 文档包含读者为当前目的所需要的信息，并尽量少包含读者不需要的信息。
        basis:
        - entity: iso-24495-1
          locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 1；PDF pp. 9–11（印刷 pp. 3–5），§5.1.1–§5.1.6
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-76611867-5bf8-4ba7-91b8-98328562a9aa
          text: relevant
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-24495-1
            locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 1；PDF pp. 9–11（印刷 pp. 3–5），§5.1.1–§5.1.6
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-e1b3aa8a-c184-4ee7-a2bd-0f9cacb93187
          text: 相关
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 相关强调内容符合读者当前信息需要；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-24495-1
        locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 1；PDF pp. 9–11（印刷 pp. 3–5），§5.1.1–§5.1.6
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-2938e52c-9172-4bc1-b3ea-a1c0476fe909
    field: record
    value:
      id: tc-2938e52c-9172-4bc1-b3ea-a1c0476fe909
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 文档的结构和设计使读者能够找到自己需要的信息。
        basis:
        - entity: iso-24495-1
          locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 2；PDF p. 11（印刷 p. 5），§5.2.1–§5.2.3
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-aeb4615f-2f52-4dfd-a5e9-380a05c4e374
          text: findable
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-24495-1
            locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 2；PDF p. 11（印刷 p. 5），§5.2.1–§5.2.3
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-290bf765-6c24-4495-9a46-ebe1e7fe462a
          text: 可找到
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 可找到强调结构和设计支持定位信息；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-24495-1
        locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 2；PDF p. 11（印刷 p. 5），§5.2.1–§5.2.3
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-973e68b6-1e0f-47a9-9ab7-0660d591969c
    field: record
    value:
      id: tc-973e68b6-1e0f-47a9-9ab7-0660d591969c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 读者能够理解自己找到的信息。
        basis:
        - entity: iso-24495-1
          locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 3
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-71fd160f-eff7-42b2-898f-4c56dd08230d
          text: understandable
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-24495-1
            locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 3
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-8da4cfa3-6bcd-4bbb-84e8-e36f3db0e01f
          text: 可理解
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 可理解强调读者对所找到信息的理解；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-24495-1
        locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 3
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-9985f5e9-89cc-4fe1-849f-c2be99f97727
    field: record
    value:
      id: tc-9985f5e9-89cc-4fe1-849f-c2be99f97727
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 读者能够使用获得的信息。
        basis:
        - entity: iso-24495-1
          locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 4 及原则关系段
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-73551363-0781-49db-b2fb-ae329c7ed476
          text: usable
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-24495-1
            locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 4 及原则关系段
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-d3c0e7d5-190f-4e6a-9b6b-4b395590ed75
          text: 可使用
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 可使用强调信息支持读者完成预期任务；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-24495-1
        locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 4 及原则关系段
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-e5c11065-dc49-4ac8-b297-aadb2edd1196
    field: record
    value:
      id: tc-e5c11065-dc49-4ac8-b297-aadb2edd1196
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在忙于其他事情时快速记下的当下想法提醒；它通常不是完整表达，需要尽快处理，值得保留的内容再改写为长期笔记。
        basis:
        - entity: ahrens-zettelkasten-interview
          locator: https://examstudyexpert.com/zettelkasten/ ; captured L91-L95
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-021f20e2-f065-4e09-ba80-2542f94f0c17
          text: fleeting note
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: ahrens-zettelkasten-interview
            locator: https://examstudyexpert.com/zettelkasten/ ; captured L91-L95
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-01f3402c-0616-4c48-8bd4-e959046120d2
          text: 闪念笔记
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 闪念笔记强调临时想法提醒与后续处理；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: ahrens-zettelkasten-interview
        locator: https://examstudyexpert.com/zettelkasten/ ; captured L91-L95
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-80512a5e-8cde-40f7-8abe-896d973ee851
    field: record
    value:
      id: tc-80512a5e-8cde-40f7-8abe-896d973ee851
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 针对读过的材料所作的笔记，保存在与永久笔记分开的地方；不能只复制摘录，应回看并思考它怎样服务于正在发展的想法，通常需要改写。
        basis:
        - entity: ahrens-zettelkasten-interview
          locator: https://examstudyexpert.com/zettelkasten/ ; captured L103-L106
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-34df14ea-ab98-4b85-a833-9d7d06773428
          text: literature note
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: ahrens-zettelkasten-interview
            locator: https://examstudyexpert.com/zettelkasten/ ; captured L103-L106
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-494f248e-2538-4d16-ac58-ff1d43102dc3
          text: 文献笔记
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 文献笔记强调针对阅读材料而作，不等同复制摘录；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: ahrens-zettelkasten-interview
        locator: https://examstudyexpert.com/zettelkasten/ ; captured L103-L106
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-5a5c6042-effa-4ebe-8a85-4560468e3adc
    field: record
    value:
      id: tc-5a5c6042-effa-4ebe-8a85-4560468e3adc
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 经过处理、值得长期保留、以他人也能理解的方式写成，并在卡片盒中继续连接和发展的笔记。
        basis:
        - entity: ahrens-zettelkasten-interview
          locator: https://examstudyexpert.com/zettelkasten/ ; captured L95-L102；https://examstudyexpert.com/zettelkasten/
            ; captured L113-L114
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-fdbe3135-7fb4-423f-bcbc-8376810130d5
          text: permanent note
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: ahrens-zettelkasten-interview
            locator: https://examstudyexpert.com/zettelkasten/ ; captured L95-L102；https://examstudyexpert.com/zettelkasten/
              ; captured L113-L114
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-3d623e69-aa38-46cc-874b-506af3f67671
          text: 永久笔记
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 永久笔记强调经过处理并长期连接发展的笔记；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: ahrens-zettelkasten-interview
        locator: https://examstudyexpert.com/zettelkasten/ ; captured L95-L102；https://examstudyexpert.com/zettelkasten/ ;
          captured L113-L114
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-362abd86-fd94-42b4-8f6e-aaca8aa3660b
    field: record
    value:
      id: tc-362abd86-fd94-42b4-8f6e-aaca8aa3660b
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 执行文件保管、销毁或移交决定的一系列过程；这些决定记录在处置授权或其他文件里。
        basis:
        - entity: iso-15489-1
          locator: https://cdn.standards.iteh.ai/samples/62542/fe383f4fe10448d5b22ce628b1542ed6/ISO-15489-1-2016.pdf；PDF p.
            10（印刷 p. 2），§3.8 disposition
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-55036694-aa11-45ee-9c54-73f98f209ffd
          text: disposition
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-15489-1
            locator: https://cdn.standards.iteh.ai/samples/62542/fe383f4fe10448d5b22ce628b1542ed6/ISO-15489-1-2016.pdf；PDF
              p. 10（印刷 p. 2），§3.8 disposition
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-47d9bbbe-00da-47da-bb2f-738a62d9bfce
          text: 处置
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 处置是文件管理中对保管、销毁或移交决定的执行，不等于删除；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-15489-1
        locator: https://cdn.standards.iteh.ai/samples/62542/fe383f4fe10448d5b22ce628b1542ed6/ISO-15489-1-2016.pdf；PDF p.
          10（印刷 p. 2），§3.8 disposition
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-9706ac56-d951-4eb6-9f27-cf7baa983a81
    field: record
    value:
      id: tc-9706ac56-d951-4eb6-9f27-cf7baa983a81
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 少数因素对总体效果起主要作用、其余多数因素作用较小的现象；本条不规定固定的 80/20 比例。
        basis:
        - entity: juran-1974-non-pareto
          locator: https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf，PDF page index 0-2（印刷页
            1-3），lines 1-21、158-168、194-209
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-75b287e7-ec70-47f6-a0be-610f6d79cc7e
          text: Pareto principle
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: juran-1974-non-pareto
            locator: https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf，PDF page index 0-2（印刷页
              1-3），lines 1-21、158-168、194-209
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-13c4955e-8bec-4ddf-8a06-f8b061153bdf
          text: 帕累托原则
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 帕累托原则是管理与质量领域对关键少数现象的行业表达，不把它改成项目选材义务；仅判断既有概念的行业表达，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: juran-1974-non-pareto
        locator: https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf，PDF page index 0-2（印刷页
          1-3），lines 1-21、158-168、194-209
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-39065fa2-767d-4606-840c-aaffa5182661
    field: record
    value:
      id: tc-39065fa2-767d-4606-840c-aaffa5182661
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 每个概念在直接上一级只能有一个上位概念的层级安排。
        basis:
        - entity: iso-25964-1
          locator: §2.34；docs/references/iso-25964.md 已核定义表
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-b3f9d941-2f49-425c-9e98-6b4e61b4444c
          text: monohierarchical structure
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.34；docs/references/iso-25964.md 已核定义表
            checked: '2026-08-29'
        - id: tm-7b60cc0e-5b50-4047-b76b-91ff8a4cbdac
          text: monohierarchy
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: dunn-bourcier-nomenclature
            locator: §6 Limitations：monohierarchical classification system每词只有一个直接broader，随后monohierarchy回指
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-9ae59983-3054-4e4b-9e59-e400bd6bffdf
          text: 单层级
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 单层级在词表领域表示每个概念只有一个直接上位概念，而非只有一层深度；仅为既有概念的模型知识译名判断，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.34；docs/references/iso-25964.md 已核定义表
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-025cc053-edb1-4def-a58f-1de00a8424a4
    field: record
    value:
      id: tc-025cc053-edb1-4def-a58f-1de00a8424a4
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 每个概念可以有多个上位概念的层级安排。
        basis:
        - entity: iso-25964-1
          locator: §2.42；docs/references/iso-25964.md 已核定义表
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-57b80a57-9a91-4320-854d-e326cb9d52fa
          text: polyhierarchical structure
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.42；docs/references/iso-25964.md 已核定义表
            checked: '2026-08-29'
        - id: tm-e2104559-047a-41be-84e5-dbe80f7d052f
          text: polyhierarchy
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §5.4.3 taxonomy；§8.3.4 Polyhierarchical Relationships及Examples109–111
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-e4c630f1-5986-4325-93a0-bc9710a3bab1
          text: 多层级
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 多层级在此表示概念允许多个上位概念，而非树的深度较大；仅为既有概念的模型知识译名判断，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.42；docs/references/iso-25964.md 已核定义表
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-98d2d330-cabe-493f-8453-104822e92a0d
    field: record
    value:
      id: tc-98d2d330-cabe-493f-8453-104822e92a0d
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 两个或更多系统或组件交换并使用所交换信息的能力。
        basis:
        - entity: iso-25964-1
          locator: §2.29；docs/references/iso-25964.md 已核定义表
          checked: '2026-08-29'
      languages:
      - language: en
        terms:
        - id: tm-fd044b18-8d70-430b-b64e-2c81f72632cf
          text: interoperability
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.29；docs/references/iso-25964.md 已核定义表
            checked: '2026-08-29'
      - language: zh-Hans
        terms:
        - id: tm-4270711e-8a98-48d0-9ba3-5a1fc25eaf22
          text: 互操作性
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 互操作性同时包括信息交换与使用，不能仅等同文件可导入；仅为既有概念的模型知识译名判断，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.29；docs/references/iso-25964.md 已核定义表
        checked: '2026-08-29'
      workflow: active
  - identity: terms/concepts/tc-79c1fd4b-5f06-4d1e-a8d8-cd323c441939
    field: record
    value:
      id: tc-79c1fd4b-5f06-4d1e-a8d8-cd323c441939
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 知识图谱中由节点表示的对象；节点及其标识用于表示和区分对象，不等于对象本身。
        basis:
        - entity: hogan-paper
          locator: P1 L72–L88；nodes represent entities 与 identity 讨论；work/reviews/2026-09-06-term-web-model-coverage.json
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-77ec69a0-9cb0-48f7-8194-1adae82bdbf6
          text: entity
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hogan-paper
            locator: P1 L72–L88；nodes represent entities 与 identity 讨论；work/reviews/2026-09-06-term-web-model-coverage.json
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-9fb55b4b-7fe8-475f-a552-10bd90c5855d
          text: 实体
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 实体是知识表示领域对被表示对象的行业称呼，不把实体等同于图节点或标识符。外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hogan-paper
        locator: P1 L72–L88；nodes represent entities 与 identity 讨论；work/reviews/2026-09-06-term-web-model-coverage.json
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-605b0308-57af-486b-81ba-81e18b993b07
    field: record
    value:
      id: tc-605b0308-57af-486b-81ba-81e18b993b07
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在属性图中，与节点或边关联、以属性名和值构成的键值对表达的信息；值的具体形态由所用属性图模型规定。
        basis:
        - entity: hogan-paper
          locator: P6 L316–L322；property graph 中 nodes/edges 关联 property–value pairs；work/reviews/2026-09-06-term-web-model-coverage.json
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-a91f7e4f-a2bb-4681-ba36-86d3529b7cbe
          text: property
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hogan-paper
            locator: P6 L316–L322；property graph 中 nodes/edges 关联 property–value pairs；work/reviews/2026-09-06-term-web-model-coverage.json
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-16fe2abb-fe52-4f08-97a4-5bb36f6c2f15
          text: 属性
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 属性是图数据模型中描述节点或边特征的信息；本条明确属性图语境，并区别属性名与其值。外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hogan-paper
        locator: P6 L316–L322；property graph 中 nodes/edges 关联 property–value pairs；work/reviews/2026-09-06-term-web-model-coverage.json
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-4f002e0f-1fe2-41e5-a15c-3cdb436b1763
    field: record
    value:
      id: tc-4f002e0f-1fe2-41e5-a15c-3cdb436b1763
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 按分类排列的概念及先组组合的表。
        basis:
        - entity: iso-25964-1
          locator: §2.6，免费样章印刷p.2
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-29e4f758-6d4f-4411-b474-e1f08b3213ae
          text: classification scheme
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.6，免费样章印刷p.2
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-4011c8e8-cd44-497e-85f0-1667007d53c7
          text: 分类表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 分类表指按分类组织的概念表，不替换成taxonomy或一般分类操作。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.6，免费样章印刷p.2
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-84906e82-1b72-4118-951c-33416d9d9bf7
    field: record
    value:
      id: tc-84906e82-1b72-4118-951c-33416d9d9bf7
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 表示一个概念的一个或多个词。
        basis:
        - entity: z39-19
          locator: §4.1 Glossary，term
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-6d783441-c3df-409b-8202-742ff6b3bfa4
          text: term
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §4.1 Glossary，term
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-868a4b9a-45b4-4d9f-b359-8de7a44f060f
          text: 词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: NISO已核term意义与原概念一致；英文名称保留，中文词在本条也包含多词表达，不冒称ISO§2.61已读。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §4.1 Glossary，term
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-c5ee911a-276c-4bc1-81e7-f651972b0830
    field: record
    value:
      id: tc-c5ee911a-276c-4bc1-81e7-f651972b0830
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 不直接用于元数据、而引导用户找到另一可用词的受控词表术语；在叙词表中通常称非首选词。
        basis:
        - entity: iso-25964-1
          locator: §2.16，免费样章印刷p.4
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-ba65904c-7386-439b-9b62-d2fbb3024a94
          text: entry term
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.16，免费样章印刷p.4
            checked: '2026-09-06'
        - id: tm-87280583-a819-4fba-a27d-83bfb9035805
          text: lead-in term
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.16，免费样章印刷p.4
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-c15bae24-b66d-4da9-bb5b-cd84d38fd50c
          text: 入口词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 入口词强调通向可用术语的检索入口，不等于所有标引词。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.16，免费样章印刷p.4
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-57a8d816-05c4-4aa9-b3da-277b5d23cc4e
    field: record
    value:
      id: tc-57a8d816-05c4-4aa9-b3da-277b5d23cc4e
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 可供基于文本的检索使用，但不供用户直接显示的标签。
        basis:
        - entity: skos
          locator: §5 Lexical Labels；skos:hiddenLabel及示例
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-9c6430b5-c331-4cf0-943a-5cae137ca58d
          text: hidden label
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: skos
            locator: §5 Lexical Labels；skos:hiddenLabel及示例
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-3c495c32-6257-4fc1-8ecf-e60a823d33da
          text: 隐藏标签
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 隐藏标签对应可检索但不直接显示的词汇标签；ISO hidden布尔输出标志只作模型背景，不声称两个接口完全等价。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: skos
        locator: §5 Lexical Labels；skos:hiddenLabel及示例
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-d58d9afb-92ca-46c1-b928-e6ea6c2a11a6
    field: record
    value:
      id: tc-d58d9afb-92ca-46c1-b928-e6ea6c2a11a6
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 写法相同而意义不同的词。
        basis:
        - entity: iso-25964-1
          locator: §2.24，免费样章印刷p.6
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-c9a7fa2f-a37c-4f88-83bd-aed4e2b88613
          text: homograph
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.24，免费样章印刷p.6
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-d4d7539d-7a93-487d-ba5b-d94d3b3fdbf0
          text: 同形异义词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 同形异义词同时保留相同字形与不同意义这两个判据。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.24，免费样章印刷p.6
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-adbb6019-db11-4d1e-a9b2-4e7a8fedd0a5
    field: record
    value:
      id: tc-adbb6019-db11-4d1e-a9b2-4e7a8fedd0a5
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 通常意义不同，但在特定受控词表中可作为同一概念标签的词。
        basis:
        - entity: iso-25964-1
          locator: §2.47，免费样章印刷p.9
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-3cd0a683-a19a-4073-8f06-87e6540ec09c
          text: quasi-synonym
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.47，免费样章印刷p.9
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-b56a70b0-92c7-460b-a1ca-9d5d5cf27dcb
          text: 准同义词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 准同义词是特定词表中的约定等价，非日常语言完全同义。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.47，免费样章印刷p.9
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-a977c939-c9fe-477b-a154-a0ccd97aa3d6
    field: record
    value:
      id: tc-a977c939-c9fe-477b-a154-a0ccd97aa3d6
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 可按形态拆成独立成分的术语；可以由一个词或多个词组成。
        basis:
        - entity: iso-25964-1
          locator: §2.9，免费样章印刷p.3
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-427e5a68-a3c5-4be6-9337-f84962686067
          text: compound term
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.9，免费样章印刷p.3
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-2d65f52c-42b6-464f-9208-f4cb567df8db
          text: 复合词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 复合词按形态可拆分确定，不仅是有空格的多词短语。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.9，免费样章印刷p.3
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-b0214996-65e1-4d37-a055-b7356a776ac0
    field: record
    value:
      id: tc-b0214996-65e1-4d37-a055-b7356a776ac0
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 可由两个或更多较简单概念组合表示的概念。
        basis:
        - entity: will-2012-iso-data-model
          locator: Compound Equivalence，L94–101，coal mining同例compound concept与complex concept回指
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-bb629eab-c872-4e13-a921-7c7577afb769
          text: complex concept
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: will-2012-iso-data-model
            locator: Compound Equivalence，L94–101，coal mining同例compound concept与complex concept回指
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-f33000a3-3b8c-467d-9731-9a83c28bfe76
          text: 复合概念
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 复合概念的旧英文complex concept在作者同段直接出现，意义与原组合概念一致，不自动新增coal mining等示例概念。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: will-2012-iso-data-model
        locator: Compound Equivalence，L94–101，coal mining同例compound concept与complex concept回指
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-6a20995f-a6b2-492a-88e9-a554c8364fe2
    field: record
    value:
      id: tc-6a20995f-a6b2-492a-88e9-a554c8364fe2
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 专门知识的范围。
        basis:
        - entity: iso-1087-2019
          locator: §3.1.4，PDFp.7/印刷p.1，注释续p.8
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-d1b26431-6581-44bf-929d-095b69ca660f
          text: domain
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-1087-2019
            locator: §3.1.4，PDFp.7/印刷p.1，注释续p.8
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-8fc9be24-693d-4905-a110-353c793cf283
          text: 领域
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 领域是专门知识范围的行业名称；本库用于说明词表覆盖范围，应用用法另说明，不等于网络域。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-1087-2019
        locator: §3.1.4，PDFp.7/印刷p.1，注释续p.8
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-a8e5c450-33ff-42e5-a352-1bbb21fcd0b5
    field: record
    value:
      id: tc-a8e5c450-33ff-42e5-a352-1bbb21fcd0b5
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 识别文档属性，通常支持定位、发现、记录、评价或选择的数据。
        basis:
        - entity: iso-25964-1
          locator: §2.33，免费样章印刷p.6
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-067d0bdf-9db2-490f-a6a8-301b3ec0ee1f
          text: metadata
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.33，免费样章印刷p.6
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-92599d5f-6dad-4f51-a4b9-379f8e14ac85
          text: 元数据
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 元数据保留文档属性描述的原语境；首选词可作元数据值是来源补充说明。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.33，免费样章印刷p.6
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-ad90ba40-f5b0-44e7-9f59-fa2783d837b3
    field: record
    value:
      id: tc-ad90ba40-f5b0-44e7-9f59-fa2783d837b3
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 一个语境中的术语或概念在另一语境中由两个或更多术语或概念表示的关系或映射。
        basis:
        - entity: iso-25964-1
          locator: §2.8，免费样章印刷p.2
          checked: '2026-09-06'
      languages:
      - language: zh-Hans
        terms:
        - id: tm-2295a8c2-8677-4bf0-97fc-b962cad6bc4a
          text: 复合等价
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 复合等价指一对多的概念或名称表示；USE+/UF+是符号，不造英文术语。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.8，免费样章印刷p.2
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-54e74c2d-103e-4935-aab7-fb44a129af69
    field: record
    value:
      id: tc-54e74c2d-103e-4935-aab7-fb44a129af69
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 类与子类之间的层级关系：子类的每个成员均属于上位类，而上位类还包含该子类以外的成员。
        basis:
        - entity: z39-19
          locator: §8.3.1与§8.3.2，印刷pp.47–48，PDFindex58–59
          checked: '2026-09-06'
      languages:
      - language: zh-Hans
        terms:
        - id: tm-0e54e5ec-61e2-412f-8e2a-1ac13804a53f
          text: 属种关系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 属种关系是类与子类的全部/部分关系，不把个别实例属于类混入；原BTG/NTG只作关系指示符。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §8.3.1与§8.3.2，印刷pp.47–48，PDFindex58–59
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-818463b8-0d48-4ddf-98fb-228ef4591308
    field: record
    value:
      id: tc-818463b8-0d48-4ddf-98fb-228ef4591308
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 整体与其组成部分之间的层级关系。
        basis:
        - entity: z39-19
          locator: §8.3.3 Whole-Part Relationships，印刷p.49
          checked: '2026-09-06'
      languages:
      - language: zh-Hans
        terms:
        - id: tm-4a9bb6d7-1099-41e8-be65-a9da97d0073a
          text: 整部关系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 整部关系保留整体/部分机制，不能把任意关联解释为部分；原BTP/NTP为符号。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §8.3.3 Whole-Part Relationships，印刷p.49
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-9fde9fd8-eb29-4477-acc1-295f9de9adf5
    field: record
    value:
      id: tc-9fde9fd8-eb29-4477-acc1-295f9de9adf5
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 一般类或类型与其个别实例之间的层级关系。
        basis:
        - entity: z39-19
          locator: §8.3.2 Instance Relationships，印刷p.48
          checked: '2026-09-06'
      languages:
      - language: zh-Hans
        terms:
        - id: tm-64b1efd6-53a5-4b7e-827c-0edfdadd6ba2
          text: 实例关系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 实例关系的两端是类与个体，不是类与子类；原BTI/NTI为符号。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §8.3.2 Instance Relationships，印刷p.48
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-a529619b-cbcb-4545-901d-54f72971e76f
    field: record
    value:
      id: tc-a529619b-cbcb-4545-901d-54f72971e76f
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在既有关系类型下，由词表管理者进一步规定的关系类型。
        basis:
        - entity: iso25964-xsd-1-4
          locator: HierarchicalRelationship/role文档注记；AssociativeRelationship/role
          checked: '2026-09-06'
      languages:
      - language: zh-Hans
        terms:
        - id: tm-dd400c8e-6f1f-4f2b-a787-1b9290e16e7d
          text: 自定义关系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 自定义关系表达类型细分机制，依据为配套工件而非未读ISO§10.4；不授权本库实际新增任何关系类型。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso25964-xsd-1-4
        locator: HierarchicalRelationship/role文档注记；AssociativeRelationship/role
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-df2d8160-1717-4372-a38f-db96925ac980
    field: record
    value:
      id: tc-df2d8160-1717-4372-a38f-db96925ac980
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 概念自身固有、可独立于特定文档语境在结构化词表中表达的关系。
        basis:
        - entity: iso-25964-1
          locator: §2.41 paradigmatic relationship / a priori relationship，印刷p.8
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-572d4ac7-3aae-4823-83e3-fddeedba662e
          text: paradigmatic relationship
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.41 paradigmatic relationship / a priori relationship，印刷p.8
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-d5659ae3-56dd-4e82-ac4e-cc45fcce05a5
          text: 聚合关系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 聚合关系保留概念内在语义，区别随文档语境形成的组合关系。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.41 paradigmatic relationship / a priori relationship，印刷p.8
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-1b0b91bc-d29e-44d4-854c-cddd05aebc13
    field: record
    value:
      id: tc-1b0b91bc-d29e-44d4-854c-cddd05aebc13
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 依赖特定表达或文献语境而形成的概念关系。
        basis:
        - entity: mazzocchi-knowledge-organization-system
          locator: §5.1 a priori/a posteriori与paradigmatic/syntagmatic段
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-ccdfadf2-0216-4f91-aa21-d7a4d1f5b8bd
          text: syntagmatic relationship
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: mazzocchi-knowledge-organization-system
            locator: §5.1 a priori/a posteriori与paradigmatic/syntagmatic段
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-3dc5c513-2684-4789-b88b-2a74897fb869
          text: 组合关系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 组合关系依语境建立，不等于同篇出现就必有语义关系；不把作者说明写成已读ISO§4.3。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: mazzocchi-knowledge-organization-system
        locator: §5.1 a priori/a posteriori与paradigmatic/syntagmatic段
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-b10cded9-f3ab-4cdd-b218-edb279779c33
    field: record
    value:
      id: tc-b10cded9-f3ab-4cdd-b218-edb279779c33
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 一种关系与其反向关系相互配对，如A以BT指向B时，B以NT反向指向A。
        basis:
        - entity: z39-19
          locator: §4.1 reciprocal；§5.4.4 relationship indicators reciprocally；§8.3
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-34ed6873-0990-469c-b505-518e69018077
          text: reciprocal
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §4.1 reciprocal；§5.4.4 relationship indicators reciprocally；§8.3
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-2509c694-0529-422a-8c8c-16b9cc377310
          text: 互反
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 互反表示反向关系配对；不把关系概念直接变成本库必须物理双写的实现规则。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §4.1 reciprocal；§5.4.4 relationship indicators reciprocally；§8.3
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-af0edf3d-0500-4fc7-bad0-39127321295c
    field: record
    value:
      id: tc-af0edf3d-0500-4fc7-bad0-39127321295c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 按上位与下位关系组织的概念结构，可含单上位或多上位安排。
        basis:
        - entity: z39-19
          locator: §8.3与§8.3.4，印刷pp.47–50
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-bbbe8ecb-22ce-4f7d-a526-5b051b058056
          text: hierarchy
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §8.3与§8.3.4，印刷pp.47–50
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-a8384214-a207-4a7c-9fd0-4313fdb5b353
          text: 层级
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 层级是上下位安排，允许多上位；不能与严格树结构无条件同义。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §8.3与§8.3.4，印刷pp.47–50
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-7d9ce2a6-2d92-49c3-8d22-c771cdaae4c3
    field: record
    value:
      id: tc-7d9ce2a6-2d92-49c3-8d22-c771cdaae4c3
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 由根节点及其子树递归组成的节点结构。
        basis:
        - entity: nist-dads-tree
          locator: Definition(1)及Formal Definition，2017-12-15
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-3b55a969-53ac-4622-ab97-d7774a558335
          text: tree
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: nist-dads-tree
            locator: Definition(1)及Formal Definition，2017-12-15
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-083afbe6-20c8-47c6-9d23-a51bdd0c2549
          text: 树
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 树保留原中文独立结构概念，按NIST定义区别于可有多上位的一般层级；英文tree为源有依据的补充形式。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: nist-dads-tree
        locator: Definition(1)及Formal Definition，2017-12-15
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-2cc8c45b-bf02-4b54-bbfc-86286dbd50d7
    field: record
    value:
      id: tc-2cc8c45b-bf02-4b54-bbfc-86286dbd50d7
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 图或树数据结构中的一个顶点。
        basis:
        - entity: nist-dads-node
          locator: Definition(1)，2004-12-17
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-17074702-584d-4331-acfa-2c2e88627670
          text: node
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: nist-dads-node
            locator: Definition(1)，2004-12-17
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-abffcb75-f9c9-43fa-bf71-798a140d5b48
          text: 节点
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 节点在本行限于图/树结构；本库以节点表示概念是应用说明，不进入NIST定义。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: nist-dads-node
        locator: Definition(1)，2004-12-17
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-6d0b88b7-c403-48bf-9579-b2d94dbf9502
    field: record
    value:
      id: tc-6d0b88b7-c403-48bf-9579-b2d94dbf9502
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在层级顶端、没有上位概念的概念。
        basis:
        - entity: iso25964-xsd-1-4
          locator: ThesaurusConceptStruct/topConcept documentation
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-2c29e44a-28e1-430a-bc45-252c6f067a30
          text: top concept
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso25964-xsd-1-4
            locator: ThesaurusConceptStruct/topConcept documentation
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-30908171-1a13-4cb7-b754-48b0014eea6f
          text: 顶层概念
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 顶层概念按没有broader确定，不是显示窗口中暂时最上的节点。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso25964-xsd-1-4
        locator: ThesaurusConceptStruct/topConcept documentation
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-6bd16590-fd5e-4cee-9c8b-881051af3706
    field: record
    value:
      id: tc-6bd16590-fd5e-4cee-9c8b-881051af3706
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 叙词表中指定的、能够作为完整叙词表运行的子集。
        basis:
        - entity: iso-25964-2
          locator: §3.46，PDFindex13/印刷p.8
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-4b576cd0-ac19-4ef6-883b-72e82977549c
          text: microthesaurus
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.46，PDFindex13/印刷p.8
            checked: '2026-09-06'
        - id: tm-c6e74d84-b72d-47ae-9b25-bc9896c878ca
          text: micro-thesaurus
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.46，PDFindex13/印刷p.8
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-39d989b6-114d-4482-823a-e6d505597c0c
          text: 微词表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 微词表强调子集可独立作为完整叙词表运行；是否实际建立子库不由词条采纳决定。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.46，PDFindex13/印刷p.8
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-81fc1070-a33d-4692-b613-751819cecc3b
    field: record
    value:
      id: tc-81fc1070-a33d-4692-b613-751819cecc3b
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 分类体系中为可重复适用的特征设置、与主表类号配合使用的表；其适用范围可为通用或限于指定主类。
        basis:
        - entity: w3c-udc-use-case
          locator: L22 special auxiliaries；L56–57 common auxiliaries及tables，L68–80组合案例
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-3fd9be57-3134-4fdb-83ac-4e4288f39ab5
          text: auxiliary table
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: w3c-udc-use-case
            locator: L22 special auxiliaries；L56–57 common auxiliaries及tables，L68–80组合案例
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-1db6403d-e157-42c0-9d03-d9c6bafaef9e
          text: 辅助表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 辅助表说明复用分类特征机制；原只通用维度、只尾部拼接过窄，固定作者案例同时展示专用与通用。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
        - id: tm-b4a8055d-5598-4ea1-bc76-e35428986632
          text: 复分表
          administrative_status: admittedTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 复分表是分类实践中以可重复特征进一步细分类号的既有中文称呼；本条与辅助表同限配合主表使用的分类表，不泛指任意再次划分。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: w3c-udc-use-case
        locator: L22 special auxiliaries；L56–57 common auxiliaries及tables，L68–80组合案例
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-2f3dc564-3adc-46d7-ba3c-4051eaaa434c
    field: record
    value:
      id: tc-2f3dc564-3adc-46d7-ba3c-4051eaaa434c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 按分类体系规则组合主号、辅助号或多个主号，以表达复合主题的记号。
        basis:
        - entity: w3c-udc-use-case
          locator: L56–80组合通用辅助号/主号与复合主题；参ISO25964-1§2.22上下文
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-c465bee5-b846-4fc6-879b-26642d41fca3
          text: synthesized notation
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: w3c-udc-use-case
            locator: L56–80组合通用辅助号/主号与复合主题；参ISO25964-1§2.22上下文
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-23343b8e-95df-4574-a499-8cdf75d77e8c
          text: 组配号
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 组配号是组合所得分类记号，区别标示分面开始的facet indicator；原ISO条目错位明确纠正。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: w3c-udc-use-case
        locator: L56–80组合通用辅助号/主号与复合主题；参ISO25964-1§2.22上下文
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-a4f76dad-bbea-4cf0-b322-1c689c380d95
    field: record
    value:
      id: tc-a4f76dad-bbea-4cf0-b322-1c689c380d95
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在建表阶段或标引、分类阶段组合受控词表中的概念、类或术语。
        basis:
        - entity: iso-25964-1
          locator: §2.44，免费样章印刷p.9
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-3b1cb85c-480e-4e19-a3ef-5b868cd6a3cb
          text: pre-coordination
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.44，免费样章印刷p.9
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-72449164-9665-4eed-bd23-9198392d3432
          text: 先组
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 先组按组合发生在构建/标引阶段界定，不把多词形式自动等同先组。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.44，免费样章印刷p.9
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-7fd3d9b0-be29-4f3c-a5a6-7817f26d9391
    field: record
    value:
      id: tc-7fd3d9b0-be29-4f3c-a5a6-7817f26d9391
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在检索时组合受控词表的首选词。
        basis:
        - entity: iso-25964-1
          locator: §2.43，免费样章印刷p.9
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-3b58953d-02b2-4956-947e-b60779dfca0d
          text: post-coordination
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-1
            locator: §2.43，免费样章印刷p.9
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-dd7d2f60-4b07-447c-bc5f-f06d5724fa19
          text: 后组
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 后组的区别在检索时组合，与先组作时点对照。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-1
        locator: §2.43，免费样章印刷p.9
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-7cee3db8-8807-48b2-9fe8-7f0fe0539272
    field: record
    value:
      id: tc-7cee3db8-8807-48b2-9fe8-7f0fe0539272
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在元数据检索语境中，用于描述、排序或筛选内容对象的一项特性，通过字段及其值表示。
        basis:
        - entity: hearst-2009-search-user-interfaces
          locator: §8.3 attribute/dimension同例；§8.6 facet/dimension/feature type
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-16a66968-e1b1-4709-9f46-a3dd2964c067
          text: attribute
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hearst-2009-search-user-interfaces
            locator: §8.3 attribute/dimension同例；§8.6 facet/dimension/feature type
            checked: '2026-09-06'
        - id: tm-a7e2d2bf-bd4f-42c6-a0dd-39cc88a90373
          text: dimension
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: hearst-2009-search-user-interfaces
            locator: §8.3 attribute/dimension同例；§8.6 facet/dimension/feature type
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-67e8828c-7806-42b2-a9f1-b0053cf14a54
          text: 属性
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 属性是内容对象的特性，不是存储字段本身；与知识图谱property另一个概念分开。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
        - id: tm-2c3da61d-f341-4d0d-9614-aefc3c6f7a3f
          text: 维度
          administrative_status: admittedTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 维度在本条仅指描述或检索内容对象的特性方面，与attribute同一受限范围；不等同所有数学维度或分面结构。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hearst-2009-search-user-interfaces
        locator: §8.3 attribute/dimension同例；§8.6 facet/dimension/feature type
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-549f2d8d-7ddd-4bd3-b6e1-74e815f9feb2
    field: record
    value:
      id: tc-549f2d8d-7ddd-4bd3-b6e1-74e815f9feb2
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用来描述一个概念并将其与相关概念区别开的表达。
        basis:
        - entity: iso-1087-2019
          locator: §3.3.1，PDFp.12/印刷p.6
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-4b5fc7e6-51b3-47af-8068-ea2df1fca97a
          text: definition
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-1087-2019
            locator: §3.3.1，PDFp.12/印刷p.6
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-7ecbf405-7181-4a27-ae54-3cc83dafd16e
          text: 定义
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 定义的意义由ISO1087支持；ISO25964的Definition类只是存放位置说明，不替代一般概念。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-1087-2019
        locator: §3.3.1，PDFp.12/印刷p.6
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-d6a34d9f-e8f9-4170-9d62-e5b3676e71d9
    field: record
    value:
      id: tc-d6a34d9f-e8f9-4170-9d62-e5b3676e71d9
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 供叙词表编辑者在编辑过程中使用的注释。
        basis:
        - entity: iso25964-xsd-1-4
          locator: EditorialNote documentation
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-7595b7a0-4cc9-4006-8158-8e6e21dc605d
          text: editorial note
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso25964-xsd-1-4
            locator: EditorialNote documentation
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-50a8107f-fb70-4df7-be97-59c8f5ac72e8
          text: 编辑注释
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 编辑注释服务编辑过程，区别供用户理解概念范围的注释。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso25964-xsd-1-4
        locator: EditorialNote documentation
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-82db3b46-353e-405f-8a8d-fd6fee70bdb5
    field: record
    value:
      id: tc-82db3b46-353e-405f-8a8d-fd6fee70bdb5
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 与首选术语同义，但在可接受性评价中被列为不宜使用的术语。
        basis:
        - entity: iso-1087-2019
          locator: §3.4.21，GSO公开HTML预览；对照§3.4.22 obsolete term
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-5ec44c1d-1d30-4952-8a28-d82bc54f7669
          text: deprecated term
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-1087-2019
            locator: §3.4.21，GSO公开HTML预览；对照§3.4.22 obsolete term
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-e1b7439c-738a-4056-9c53-8e96b4b7d5ef
          text: 废弃词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 废弃词指不宜使用的名称评价，不自动包含删除、保留或替代链的项目操作；与不再常用的obsolete区别。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-1087-2019
        locator: §3.4.21，GSO公开HTML预览；对照§3.4.22 obsolete term
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-504af76c-f69e-469e-8e73-239f2fd3da99
    field: record
    value:
      id: tc-504af76c-f69e-469e-8e73-239f2fd3da99
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 表示概念或术语在管理过程中所处阶段的属性。
        basis:
        - entity: iso25964-xsd-1-4
          locator: ThesaurusConceptStruct/status与ThesaurusTerm/status文档注记
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-da14faa1-b603-4b39-9e6c-37a797c42b2b
          text: status
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso25964-xsd-1-4
            locator: ThesaurusConceptStruct/status与ThesaurusTerm/status文档注记
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-f9159807-4154-4be9-8a5c-4039896902fa
          text: 状态
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 状态是阶段属性，来源示例值不覆盖本库状态机。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso25964-xsd-1-4
        locator: ThesaurusConceptStruct/status与ThesaurusTerm/status文档注记
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-f4802cd3-fba8-4bb1-89a0-121eebbf1fc6
    field: record
    value:
      id: tc-f4802cd3-fba8-4bb1-89a0-121eebbf1fc6
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 词表已发布或提供的各个版本的记录，说明版本间的区别以及各版本是否仍为现行。
        basis:
        - entity: will-2012-iso-data-model
          locator: Version History，L145–147，自然英文version history直接出现
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-ec43572b-e2e5-4c4a-8fb1-6be8931c3635
          text: version history
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: will-2012-iso-data-model
            locator: Version History，L145–147，自然英文version history直接出现
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-9ac2e455-f438-460f-ad02-baf7377a105d
          text: 版本历史
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 版本历史记录词表整体版次，非单条术语的变更历史；不再依靠CamelCase拆词推断形式。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: will-2012-iso-data-model
        locator: Version History，L145–147，自然英文version history直接出现
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-d529a566-45fc-44f0-8b92-0eca58807137
    field: record
    value:
      id: tc-d529a566-45fc-44f0-8b92-0eca58807137
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 选择一个词进入受控词表的理由或支持。
        basis:
        - entity: z39-19
          locator: §5.3.5 Warrant，印刷p.16
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-1bf1d191-63fe-4c9e-9761-a2543c13f382
          text: warrant
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §5.3.5 Warrant，印刷p.16
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-f188b119-c518-45fa-986c-67d6f6801238
          text: 依据
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 依据在此限定收词选择，不泛化成任意字段basis。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §5.3.5 Warrant，印刷p.16
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-8b56b1d2-7fd1-499b-8085-a9dd926e4c28
    field: record
    value:
      id: tc-8b56b1d2-7fd1-499b-8085-a9dd926e4c28
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 先把主题分析为基本概念或分面，再依规定组合次序综合表示主题的分类方法。
        basis:
        - entity: hjorland-facet-analysis
          locator: §3 Basic principles of facet analysis
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-9c96c16a-7bfc-4949-8ebb-1d44e3ae2d49
          text: analytico-synthetic classification
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hjorland-facet-analysis
            locator: §3 Basic principles of facet analysis
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-5a5ad88a-778f-4cb4-ae7f-3e586fc400a2
          text: 分析综合式分类
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 分析综合式分类保留先分析后综合机制；作者后续原文可作定义依据，不伪报已读Ranganathan1957。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hjorland-facet-analysis
        locator: §3 Basic principles of facet analysis
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-b888a0b9-0011-4e55-b6a5-bb01e56b79aa
    field: record
    value:
      id: tc-b888a0b9-0011-4e55-b6a5-bb01e56b79aa
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 要求分类法能够在数组和链中容纳新增类目及类号，并保持既有安排的准则。
        basis:
        - entity: kaula-1980-canons
          locator: §2，印刷p.118；§7/7.1/7.2，印刷p.125
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-80141b21-b90d-4ca3-8735-7a022c1a88b1
          text: canon of hospitality
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: kaula-1980-canons
            locator: §2，印刷p.118；§7/7.1/7.2，印刷p.125
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-4fa46a60-3253-406e-b720-84673ef1bdc4
          text: 好客准则
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 好客准则在分类学中指容纳新类目的能力，保留数组和链两个方面，不新增两种概念。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: kaula-1980-canons
        locator: §2，印刷p.118；§7/7.1/7.2，印刷p.125
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-f91d813f-7dfd-4aae-9198-756996799dd3
    field: record
    value:
      id: tc-f91d813f-7dfd-4aae-9198-756996799dd3
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 把知识领域作为社会中的思想或话语共同体，结合社会学和认识论立场研究其知识组织过程与系统的方法。
        basis:
        - entity: hjorland-domain-analysis
          locator: §1.1/1.2/1.4/2.1/4.7/7；作者实际网页正文
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-5efaa936-a3bb-4f9a-b5c9-e2a3d64af7de
          text: domain analysis
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hjorland-domain-analysis
            locator: §1.1/1.2/1.4/2.1/4.7/7；作者实际网页正文
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-aa71dcf0-b589-4daf-8125-e27672bebe75
          text: 领域分析
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 领域分析保留LIS中的共同体、专门知识与认识论机制；不换成软件工程domain analysis，不将没有唯一正确分类写成绝对定律。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hjorland-domain-analysis
        locator: §1.1/1.2/1.4/2.1/4.7/7；作者实际网页正文
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-b96d261a-9203-4f68-8b78-92e2667818ea
    field: record
    value:
      id: tc-b96d261a-9203-4f68-8b78-92e2667818ea
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 给定分类系统中无法得到正式表示的类目。
        basis:
        - entity: star-bowker-2007-enacting-silence
          locator: 原作者论文Abstract，Ethics and Information Technology9(2007)273–280
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-135147b0-7149-4c14-9d10-d4863a83edf2
          text: residual category
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: star-bowker-2007-enacting-silence
            locator: 原作者论文Abstract，Ethics and Information Technology9(2007)273–280
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-ef7fbfce-26f3-4f02-aa2d-ec9380f73b15
          text: 剩余类目
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 剩余类目以分类无法正式表示为边界；旧其他/杂项是例子，大小必然说明失效的断言没有随定义采纳。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: star-bowker-2007-enacting-silence
        locator: 原作者论文Abstract，Ethics and Information Technology9(2007)273–280
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-d123d909-3897-427f-9e04-e31d9072176c
    field: record
    value:
      id: tc-d123d909-3897-427f-9e04-e31d9072176c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 分析文档主题、识别概念，并分配相应标引词以便检索的活动。
        basis:
        - entity: iso-25964-2
          locator: §3.36，PDFp.12，原始读取L470–486
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-f8d9b426-d08f-4ea6-a77d-ca28e4261912
          text: indexing
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.36，PDFp.12，原始读取L470–486
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-8d8dd91c-4bfe-42e2-84b3-f30e00b13677
          text: 标引
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 标引既有主题分析又有分配术语；引用实际已读Part2定义，不把原Part1定位伪称重读。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.36，PDFp.12，原始读取L470–486
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-7e07c6f9-8677-4b87-8e32-e23d72dbfe64
    field: record
    value:
      id: tc-7e07c6f9-8677-4b87-8e32-e23d72dbfe64
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在标引过程中分配给文档的术语。
        basis:
        - entity: iso-25964-2
          locator: §3.35，PDFp.12，L470–473
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-0a9be29e-5fb3-4d41-b287-80801423734c
          text: index term
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.35，PDFp.12，L470–473
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-f997b0b2-4bfa-4973-90c8-dc07241e3d22
          text: 标引词
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 标引词由分配行为和文档对象界定；keyword/tag宽泛比较单列而不当必要定义。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.35，PDFp.12，L470–473
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-c96ff99a-aef7-4d8d-b4d5-2c3e2835a64b
    field: record
    value:
      id: tc-c96ff99a-aef7-4d8d-b4d5-2c3e2835a64b
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 三个或更多词表的概念之间协调维护的一组映射。
        basis:
        - entity: iso-25964-2
          locator: §3.42，PDFp.12，L512–518
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-0b3df564-f31a-41b9-bcd8-ae62a8b5b2aa
          text: mapping cluster
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.42，PDFp.12，L512–518
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-3911501b-963b-4f98-abdb-d9f4cc97b7e5
          text: 映射簇
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 映射簇是协调的多词表映射集合，保留原三个或更多的源定义条件。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.42，PDFp.12，L512–518
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-dc56c863-cea8-485d-afcd-c606ce2a8a4b
    field: record
    value:
      id: tc-dc56c863-cea8-485d-afcd-c606ce2a8a4b
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 两个或更多结构化词表中的概念之间映射的表。
        basis:
        - entity: iso-25964-2
          locator: §3.21，PDFp.9，L360–363
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-145bf65b-7bb4-4d85-9511-95c04d9dd084
          text: crosswalk
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.21，PDFp.9，L360–363
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-5976ab3d-1bf1-424f-af90-3fc111527a8e
          text: 对照表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 对照表严格指原词表层crosswalk；不复用已撤的metadata-crosswalk提案ID或更换概念。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.21，PDFp.9，L360–363
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-14b64c1a-938e-4d43-8e05-e18e0dd4e4f3
    field: record
    value:
      id: tc-14b64c1a-938e-4d43-8e05-e18e0dd4e4f3
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 映射关系中提供被映射概念、作为出发端的词表。
        basis:
        - entity: iso-25964-2
          locator: §3.27，PDFp.10，L401–405 source/target两端语境
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-2549ff94-fbe5-4854-bbba-79a658e6e46a
          text: source vocabulary
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.27，PDFp.10，L401–405 source/target两端语境
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-101132c3-86ad-4115-8d07-44caba815192
          text: 源词表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 源词表是映射中的一端角色；原并列两项分开，不当同义词，不需制造未读独立条款。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.27，PDFp.10，L401–405 source/target两端语境
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-b98ed928-3bbd-42a8-8f7f-b447c735b4c7
    field: record
    value:
      id: tc-b98ed928-3bbd-42a8-8f7f-b447c735b4c7
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 映射关系中提供对应概念、作为目标端的词表。
        basis:
        - entity: iso-25964-2
          locator: §3.27，PDFp.10，L401–405 source/target两端语境
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-7f2a566a-083a-48ee-9396-6cd2b7f100ff
          text: target vocabulary
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-25964-2
            locator: §3.27，PDFp.10，L401–405 source/target两端语境
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-a946b241-c351-47b7-b4d8-e67a02a83c2c
          text: 目标词表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 目标词表是映射中的一端角色；原并列两项分开，不当同义词，不需制造未读独立条款。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-25964-2
        locator: §3.27，PDFp.10，L401–405 source/target两端语境
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-5d5225be-ab9d-44e4-866b-e321c998d766
    field: record
    value:
      id: tc-5d5225be-ab9d-44e4-866b-e321c998d766
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 源词表与目标词表中的两个概念具有相同范围的等价关系。
        basis:
        - entity: will-2009-skos-iso
          locator: Mapping between thesauri a–c；L131–140
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-730b11b7-c904-4533-bdd1-ecaea57a3bf3
          text: exact equivalence
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: will-2009-skos-iso
            locator: Mapping between thesauri a–c；L131–140
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-a10f14d1-2756-456f-90b1-754ad286e2a0
          text: 精确等价
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 精确等价按Will2009明确范围判据解释；这是个人作者解释，不伪称ISO2013§11逐项核实或SKOS属性公理。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: will-2009-skos-iso
        locator: Mapping between thesauri a–c；L131–140
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-11c76a96-ef73-4369-9650-0f044c8eb0e7
    field: record
    value:
      id: tc-11c76a96-ef73-4369-9650-0f044c8eb0e7
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 两个概念的范围有交集，但各自仍有另一概念未涵盖部分的等价关系。
        basis:
        - entity: will-2009-skos-iso
          locator: Mapping between thesauri a–c；L131–140
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-4f940b74-b5de-43bc-8e22-502a17babe23
          text: inexact equivalence
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: will-2009-skos-iso
            locator: Mapping between thesauri a–c；L131–140
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-04654a55-fb23-444b-a74f-36f6a8793cc3
          text: 不精确等价
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 不精确等价按Will2009明确范围判据解释；这是个人作者解释，不伪称ISO2013§11逐项核实或SKOS属性公理。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: will-2009-skos-iso
        locator: Mapping between thesauri a–c；L131–140
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-531f3821-4ee7-4345-831e-778371f56302
    field: record
    value:
      id: tc-531f3821-4ee7-4345-831e-778371f56302
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 两个概念范围不相同，且一个概念范围完全包含在另一概念范围内的等价关系。
        basis:
        - entity: will-2009-skos-iso
          locator: Mapping between thesauri a–c；L131–140
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-d33a709f-8a18-4c9e-8209-9d354dce8e4b
          text: partial equivalence
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: will-2009-skos-iso
            locator: Mapping between thesauri a–c；L131–140
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-8065ee4d-eebb-493d-ad78-20ad9edc976e
          text: 部分等价
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 部分等价按Will2009明确范围判据解释；这是个人作者解释，不伪称ISO2013§11逐项核实或SKOS属性公理。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: will-2009-skos-iso
        locator: Mapping between thesauri a–c；L131–140
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-4d6508b0-a334-4017-aa7d-205469ae902e
    field: record
    value:
      id: tc-4d6508b0-a334-4017-aa7d-205469ae902e
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 连接不同词表中范围较宽与较窄概念的有向映射；按目标相对源概念的范围区分宽义或狭义方向。
        basis:
        - entity: clarke-information-retrieval-thesaurus
          locator: §3.2/Figure3
          checked: '2026-09-06'
        - entity: dnb-marc-2014-05
          locator: §1 BACKGROUND，BM/NM
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-f898b175-8fa7-45c1-94ef-c548e0928757
          text: hierarchical mapping
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: clarke-information-retrieval-thesaurus
            locator: §3.2/Figure3
            checked: '2026-09-06'
          - entity: dnb-marc-2014-05
            locator: §1 BACKGROUND，BM/NM
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-d1c40f39-ba5d-446c-93dc-7d232d73facb
          text: 层级映射
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 层级映射保留跨词表上下位及方向；不是把ISO原未读目录冒称正文。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: clarke-information-retrieval-thesaurus
        locator: §3.2/Figure3
        checked: '2026-09-06'
      - entity: dnb-marc-2014-05
        locator: §1 BACKGROUND，BM/NM
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-64b64810-6aef-4db4-b09f-aa169129c448
    field: record
    value:
      id: tc-64b64810-6aef-4db4-b09f-aa169129c448
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 连接不同词表中语义相关概念的映射；两端不属于同义、近义或宽窄关系。
        basis:
        - entity: clarke-information-retrieval-thesaurus
          locator: §3.2/Figure3
          checked: '2026-09-06'
        - entity: dnb-marc-2014-05
          locator: §1 BACKGROUND，RM
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-d61bdf72-b103-4fd6-b4dd-75cf1bd7efdb
          text: associative mapping
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: clarke-information-retrieval-thesaurus
            locator: §3.2/Figure3
            checked: '2026-09-06'
          - entity: dnb-marc-2014-05
            locator: §1 BACKGROUND，RM
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-f3dee102-5326-406c-a50e-0035c274fb25
          text: 相关映射
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 相关映射按原跨词表相关范围解释，排除等价与层级；不把RM代码新增为英文术语。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: clarke-information-retrieval-thesaurus
        locator: §3.2/Figure3
        checked: '2026-09-06'
      - entity: dnb-marc-2014-05
        locator: §1 BACKGROUND，RM
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-bf5e9356-ac91-49ae-9be3-8196dd66167c
    field: record
    value:
      id: tc-bf5e9356-ac91-49ae-9be3-8196dd66167c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 指定一个词表作为中心，其他参与词表通过与中心建立概念映射而相互衔接的结构。
        basis:
        - entity: zeng-interoperability
          locator: §5.2 Models of mapping process；Table2，期刊2019p.138
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-9a48db30-ee9b-44c4-8476-fff03dcf758f
          text: hub structure
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: zeng-interoperability
            locator: §5.2 Models of mapping process；Table2，期刊2019p.138
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-bb2e31d0-f6c8-4913-9ed3-a7cde4cb69bd
          text: 中心辐射
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 中心辐射限定参与映射结构的词表，不要求世界上所有词表或所有非中心词表互相直接映射。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: zeng-interoperability
        locator: §5.2 Models of mapping process；Table2，期刊2019p.138
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-e340f2b4-4515-4203-b5d1-8bafee5af81a
    field: record
    value:
      id: tc-e340f2b4-4515-4203-b5d1-8bafee5af81a
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 一个学科或职业领域内的知识总和。
        basis:
        - entity: swebok
          locator: 官方页面Focus on Generally Accepted Knowledge；实际urllib读取
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-96fe4b79-c997-4371-be2c-34cffcfa045c
          text: body of knowledge
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: swebok
            locator: 官方页面Focus on Generally Accepted Knowledge；实际urllib读取
            checked: '2026-09-06'
        - id: tm-4fe0093b-b34e-4012-b499-5fede4796ac8
          text: BoK
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: swebok
            locator: 官方页面Focus on Generally Accepted Knowledge；实际urllib读取
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-7e28b4bb-070a-496c-a255-42b104a2f334
          text: 知识体系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 知识体系指知识总和，不是Guide的结构化清单；Guide仅描述其中普遍接受的部分。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: swebok
        locator: 官方页面Focus on Generally Accepted Knowledge；实际urllib读取
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-3945b496-c4ac-4553-81ad-4c6dab62d81c
    field: record
    value:
      id: tc-3945b496-c4ac-4553-81ad-4c6dab62d81c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: CS2023知识模型中一组相互关联的知识单元。
        basis:
        - entity: cs2023
          locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-fefcd455-00ba-430b-9a70-6a62d846f22c
          text: knowledge area
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: cs2023
            locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
            checked: '2026-09-06'
        - id: tm-886ced2e-3c75-4147-9fda-ad2d6197f9db
          text: KA
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: cs2023
            locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-1e9a4505-f837-4791-b088-dbf23a42b1a5
          text: 知识领域
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 知识领域在此限定来源模型分组，不外推出所有知识体系固定层数。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-89c27e71-9c5a-4e5e-a588-15c0ae59345d
    field: record
    value:
      id: tc-89c27e71-9c5a-4e5e-a588-15c0ae59345d
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: CS2023知识模型中一组相关主题以及这些主题的学习成果。
        basis:
        - entity: cs2023
          locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-41116f5f-b8a3-4a24-ba19-d630df03609c
          text: knowledge unit
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: cs2023
            locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
            checked: '2026-09-06'
        - id: tm-706fc397-2755-416b-8987-c49b655a6257
          text: KU
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: cs2023
            locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-30d3ded1-73eb-4069-911b-4a8c7615a2b8
          text: 知识单元
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 知识单元不仅是主题簇，补足来源明确的学习成果。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-c5f9771f-7271-4128-854d-88b12df9f7ed
    field: record
    value:
      id: tc-c5f9771f-7271-4128-854d-88b12df9f7ed
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: CS2023知识单元内的知识主题，按课程模型标为核心或选修。
        basis:
        - entity: cs2023
          locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-dddee160-7342-44b8-8fe9-6eb8c6e47880
          text: topic
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: cs2023
            locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-58846829-6118-4a4a-b97c-8ebb5f11ede7
          text: 主题
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 主题在本行限知识单元组成内容，核心/选修为来源课程属性，不改变本库topics层级或状态。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-fbe9f215-a5f4-4292-92fa-b734f6c4b3ee
    field: record
    value:
      id: tc-fbe9f215-a5f4-4292-92fa-b734f6c4b3ee
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在大多数项目的大多数情况下适用，且其价值和作用获得广泛共识的知识。
        basis:
        - entity: swebok
          locator: 官方FAQ How do you define generally accepted knowledge?；实际urllib读取
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-192f1290-b8f5-4bc8-88e1-e9e59f3c076b
          text: generally accepted knowledge
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: swebok
            locator: 官方FAQ How do you define generally accepted knowledge?；实际urllib读取
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-87f6f03d-4e23-47f5-bf01-a50df55d039e
          text: 普遍接受的知识
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 普遍接受的知识保持SWEBOK所引PMI语境，不要求所有项目统一应用；删除全部知识体系只收此子集的旧混淆。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: swebok
        locator: 官方FAQ How do you define generally accepted knowledge?；实际urllib读取
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-42c4b942-41ba-486e-903d-1f2f18e37e45
    field: record
    value:
      id: tc-42c4b942-41ba-486e-903d-1f2f18e37e45
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 由十五个元素构成的通用元数据元素集。
        basis:
        - entity: dcmi-metadata-terms
          locator: §1 Introduction；/elements/1.1十五元素集说明
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-b85464df-26a7-4638-91c8-5444d5bb0b22
          text: Dublin Core Metadata Element Set
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: dcmi-metadata-terms
            locator: §1 Introduction；/elements/1.1十五元素集说明
            checked: '2026-09-06'
        - id: tm-844d9f9e-7c57-4bcb-9f9f-434c46fd2129
          text: Dublin Core
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: dcmi-metadata-terms
            locator: §1 Introduction；/elements/1.1十五元素集说明
            checked: '2026-09-06'
      basis:
      - entity: dcmi-metadata-terms
        locator: §1 Introduction；/elements/1.1十五元素集说明
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-30abb1cd-3364-4b41-a0e9-e0b8338aa348
    field: record
    value:
      id: tc-30abb1cd-3364-4b41-a0e9-e0b8338aa348
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 被元数据描述的对象，例如文档、图像、数据集和软件。
        basis:
        - entity: dcmi-metadata-terms
          locator: §1 Introduction and Definitions；资源描述语境
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-e034d071-30c6-4f9d-ad39-0c283caceccf
          text: resource
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: dcmi-metadata-terms
            locator: §1 Introduction and Definitions；资源描述语境
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-58221260-71b0-4fe5-a010-49fa7a359bb7
          text: 资源
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 资源以被描述对象为范围，示例不是封闭枚举，不引入rdfs:Resource类身份。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: dcmi-metadata-terms
        locator: §1 Introduction and Definitions；资源描述语境
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-56bf269d-a675-4fc3-a2c1-b1f38a734d81
    field: record
    value:
      id: tc-56bf269d-a675-4fc3-a2c1-b1f38a734d81
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 知识库中可独立引用、可独立标引的最小内容单位；有标题，并围绕一个主题组织。
        basis:
          project:
            approval: decision-term-data-values
            origin:
              commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
              file: docs/design/model/content-model.md
              locator: 内容单元；并参docs/decisions/form-independence.md后果
            rationale: 既有项目定义，DITA只作参考，不冒充外部同概念定义
      languages:
      - language: zh-Hans
        terms:
        - id: tm-55467569-4a21-4fae-a9ad-ef64e59f47f3
          text: 内容单元
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 内容单元继承现行项目模型与form-independence决定，不等同DITA topic；没有已确认英文形式，不补造英文。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
        project:
          approval: decision-term-data-values
          origin:
            commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
            file: docs/design/model/content-model.md
            locator: 内容单元；并参docs/decisions/form-independence.md后果
          rationale: 既有项目定义，DITA只作参考，不冒充外部同概念定义
      workflow: active
  - identity: terms/concepts/tc-327c7d8a-74ac-42b2-9022-da47959a339e
    field: record
    value:
      id: tc-327c7d8a-74ac-42b2-9022-da47959a339e
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在一门学科的证明中作为直接起点，不由更先命题证明的基本命题。
        basis:
        - entity: aristotle-posterior-analytics-mure
          locator: BookI Part2 immediate proposition；Part3
          checked: '2026-09-06'
        - entity: aristotle-metaphysics-ross
          locator: BookI Part2/7 first principles
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-04fb5e11-67df-42c5-a27f-634508227d21
          text: first principle
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: aristotle-posterior-analytics-mure
            locator: BookI Part2 immediate proposition；Part3
            checked: '2026-09-06'
          - entity: aristotle-metaphysics-ross
            locator: BookI Part2/7 first principles
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-2ef489fa-422e-4a9c-94d8-4a32b003561e
          text: 第一原理
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 第一原理保留证明起点概念，不扩大成一般拆解技巧，也不意味着不可质疑或不需认识依据。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: aristotle-posterior-analytics-mure
        locator: BookI Part2 immediate proposition；Part3
        checked: '2026-09-06'
      - entity: aristotle-metaphysics-ross
        locator: BookI Part2/7 first principles
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-fd033cdd-75b1-455c-9b39-431d1b9f3747
    field: record
    value:
      id: tc-fd033cdd-75b1-455c-9b39-431d1b9f3747
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 对设计系统或人工制品时所作选择及其背后推理的明确表达。
        basis:
        - entity: buckingham-shum-1995-design-rationale
          locator: KMI-95-14摘要首句
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-f5b9ffce-b288-452a-b7db-9310c5d4430d
          text: design rationale
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: buckingham-shum-1995-design-rationale
            locator: KMI-95-14摘要首句
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-aba00e29-f04b-459b-9fff-08488ae115a2
          text: 设计理由
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 设计理由是理由与推理的表示，不限软件架构ADR或IBIS文档格式。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: buckingham-shum-1995-design-rationale
        locator: KMI-95-14摘要首句
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-a64c6780-fab4-4422-86ce-d8590dae3e52
    field: record
    value:
      id: tc-a64c6780-fab4-4422-86ce-d8590dae3e52
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 决定记录被后续决定取代，但仍保留供查阅的状态。
        basis:
        - entity: nygard-2011-architecture-decisions
          locator: 正文旧决定保留并mark superseded段
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-69349502-3d1e-4e46-b82f-851ba3f2360b
          text: superseded
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: nygard-2011-architecture-decisions
            locator: 正文旧决定保留并mark superseded段
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-1869ad52-b5a3-4232-bf4f-2af24209e450
          text: 被替代
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 被替代保留ADR语境；不把来源状态扩展为任意项目对象deprecated。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: nygard-2011-architecture-decisions
        locator: 正文旧决定保留并mark superseded段
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-c484ee2c-a757-4f0f-9113-d2eda506c1bf
    field: record
    value:
      id: tc-c484ee2c-a757-4f0f-9113-d2eda506c1bf
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 规定结构化内容允许包含哪些组成部分，以及其组合、次序与重复方式的约束。
        basis:
        - entity: w3c-xml-1-0
          locator: §3.2.1 Element Content，允许类型/次序及重复规则
          checked: '2026-09-06'
        - entity: dita
          locator: DITA1.3 §2.6.3.1 Content models defined as entities
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-c89a4642-bfe3-4c06-8fcf-ee648ef2dada
          text: content model
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: w3c-xml-1-0
            locator: §3.2.1 Element Content，允许类型/次序及重复规则
            checked: '2026-09-06'
          - entity: dita
            locator: DITA1.3 §2.6.3.1 Content models defined as entities
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-94f6f1e0-2b90-4a19-852d-0b812a36abf6
          text: 内容模型
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 内容模型保留原SGML/DITA结构化内容语境；不换成CMS业务实体模型，原SGML来源只保留历史。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: w3c-xml-1-0
        locator: §3.2.1 Element Content，允许类型/次序及重复规则
        checked: '2026-09-06'
      - entity: dita
        locator: DITA1.3 §2.6.3.1 Content models defined as entities
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-c99988e5-3f77-492b-bd6e-aeca8e11ff6f
    field: record
    value:
      id: tc-c99988e5-3f77-492b-bd6e-aeca8e11ff6f
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 围绕知识及其文献表示进行描述、标引、分类和组织的活动，以及支持这些活动的系统。
        basis:
        - entity: hjorland-knowledge-organization
          locator: §1 Introduction末两段，KOP与KOS
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-8d5071d7-c12a-4c9c-bca1-e8c34f309cb5
          text: knowledge organization
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hjorland-knowledge-organization
            locator: §1 Introduction末两段，KOP与KOS
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-2a5b2ad3-d169-488b-b6ad-2498b42dc07e
          text: 知识组织
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 知识组织包括过程和系统两方面；KOS只指系统，不自动与整个KO名称同义。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hjorland-knowledge-organization
        locator: §1 Introduction末两段，KOP与KOS
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-2cc8a5dc-aa02-43fd-9cd7-f7fd9f3c3382
    field: record
    value:
      id: tc-2cc8a5dc-aa02-43fd-9cd7-f7fd9f3c3382
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在美国诽谤法语境中，因广泛名望或影响而具有一般公众人物地位，或因在某项公共争议中承担突出角色而仅就相关问题具有公众人物地位的人。
        basis:
        - entity: gertz-1974
          locator: 多数意见345、351–352页；一般声名/特定公共争议与发表作品反例
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-6f053261-8f43-4149-b2f6-3bf771797ecf
          text: public figure
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: gertz-1974
            locator: 多数意见345、351–352页；一般声名/特定公共争议与发表作品反例
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-cfe309d6-ff92-46fb-95ad-f8f58a4c3d87
          text: 公众人物
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 公众人物是此美国诽谤法语境的既有中文名；作者/维护者身份不自动达到法律门槛。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: gertz-1974
        locator: 多数意见345、351–352页；一般声名/特定公共争议与发表作品反例
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-9e03d16f-3787-4d16-9316-c46a686e0c03
    field: record
    value:
      id: tc-9e03d16f-3787-4d16-9316-c46a686e0c03
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在所描述领域中作为单个对象识别的对象，而不是概括一类对象的类。
        basis:
        - entity: owl2-primer
          locator: §3/4.1/4.7 对象、类与不同名称不保证不同个体
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-bb67e2c7-8ddc-4400-8ef4-eebad39d015a
          text: individual
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: owl2-primer
            locator: §3/4.1/4.7 对象、类与不同名称不保证不同个体
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-5a9478c7-39d8-4cc8-b1b2-acfa722afe7a
          text: 个体
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 个体不限自然人；名称规范表收录是项目用法，不作为一般定义必要条件。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: owl2-primer
        locator: §3/4.1/4.7 对象、类与不同名称不保证不同个体
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-ceeab73a-dc10-4197-8bc0-8074a1eaba15
    field: record
    value:
      id: tc-ceeab73a-dc10-4197-8bc0-8074a1eaba15
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 一个集合的非空子集所组成的集合，各子集两两不相交，且并集等于原集合。
        basis:
        - entity: cornell-cs3110-2012-partition
          locator: Recitation14首段
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-d2a7e27b-39b8-46db-b043-5b4909291305
          text: partition
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: cornell-cs3110-2012-partition
            locator: Recitation14首段
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-c8657af5-0a96-4208-a590-068abdaa6ecf
          text: 划分
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 划分保留集合论的非空、互斥和覆盖条件，不是磁盘分区或任意分类操作。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: cornell-cs3110-2012-partition
        locator: Recitation14首段
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-9e701a8f-b994-4a0d-8eab-3ea769ae1b6c
    field: record
    value:
      id: tc-9e701a8f-b994-4a0d-8eab-3ea769ae1b6c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 按内容性质及其新闻或知识表达特征区分的文本类别。
        basis:
        - entity: iptc-genre
          locator: NewsCodes Guidelines §1.1 Descriptive NewsCodes，Genre整体说明
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-9fe850d2-b2dc-47ac-a0c7-a7e2a4967744
          text: genre
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iptc-genre
            locator: NewsCodes Guidelines §1.1 Descriptive NewsCodes，Genre整体说明
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-af21a492-0a41-4c6a-aab3-9b86dd6d740d
          text: 体裁
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 体裁对应IPTC总体性质说明，本库genre选作者立场子集；Diátaxis需求属于另一组织依据，不作genre定义或英文同义证据。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iptc-genre
        locator: NewsCodes Guidelines §1.1 Descriptive NewsCodes，Genre整体说明
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-1f71845d-b74c-4a84-84c8-3976145bd5f6
    field: record
    value:
      id: tc-1f71845d-b74c-4a84-84c8-3976145bd5f6
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用于记录问题情形或症状、可能原因及纠正办法的DITA主题类型。
        basis:
        - entity: dita
          locator: DITA1.3 §2.7.1.6 dita-troubleshooting-topic.html首段及信息类型结构
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-948869da-f697-4671-b64a-d0fcc988e012
          text: troubleshooting
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: dita
            locator: DITA1.3 §2.7.1.6 dita-troubleshooting-topic.html首段及信息类型结构
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-ec8494d2-3dc5-4059-88c7-c6b8cb0e7770
          text: 排障
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 排障在原行指承载纠正信息的主题类型，不偷偷换成一般排障活动；原因与办法可未知。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: dita
        locator: DITA1.3 §2.7.1.6 dita-troubleshooting-topic.html首段及信息类型结构
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-2eb24dc0-1754-4f0b-a8c9-7239f29c1943
    field: record
    value:
      id: tc-2eb24dc0-1754-4f0b-a8c9-7239f29c1943
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 高度个人化、植根于行动和经验，难以形式化和交流的知识。
        basis:
        - entity: nonaka-toyama-konno-managing-industrial-knowledge
          locator: 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-5d81868a-1cfc-4d4d-aca9-07b816ae464b
          text: tacit knowledge
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: nonaka-toyama-konno-managing-industrial-knowledge
            locator: 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-4a653060-87cf-44bb-bbad-9ef409ef92d1
          text: 隐性知识
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 隐性知识是知识管理中对应既有英文概念的行业表达；替代已读作者章节不伪称Nonaka1991原文已读。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: nonaka-toyama-konno-managing-industrial-knowledge
        locator: 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-78034548-e62f-4b31-9921-5b22e661d1ff
    field: record
    value:
      id: tc-78034548-e62f-4b31-9921-5b22e661d1ff
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 能够用正式、系统的语言表达，并较容易处理、传递和存储的知识。
        basis:
        - entity: nonaka-toyama-konno-managing-industrial-knowledge
          locator: 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-91d7f224-0be5-401a-8c0e-4a0abfe252f5
          text: explicit knowledge
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: nonaka-toyama-konno-managing-industrial-knowledge
            locator: 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-d140d129-94ad-47e1-9181-60fb0d66c2cb
          text: 显性知识
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 显性知识是知识管理中对应既有英文概念的行业表达；替代已读作者章节不伪称Nonaka1991原文已读。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: nonaka-toyama-konno-managing-industrial-knowledge
        locator: 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-505c5536-a7dd-4100-999a-fe0472b66b1c
    field: record
    value:
      id: tc-505c5536-a7dd-4100-999a-fe0472b66b1c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 为快速查阅而汇总信息的简明资料。
        basis:
        - entity: american-heritage-dictionary-5-cheat-sheet
          locator: https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0；Fifth Edition ©2022，cheat
            sheet义项2
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-98076d19-5e2f-419d-82a4-353f20652a57
          text: cheat sheet
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: american-heritage-dictionary-5-cheat-sheet
            locator: https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0；Fifth Edition ©2022，cheat
              sheet义项2
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-2923a9eb-c720-4de1-8491-c7e6665243a6
          text: 速查表
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 速查表是技术文档中cheat sheet的惯用表达；不把任何笔记集或作弊材料纳入此概念。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: american-heritage-dictionary-5-cheat-sheet
        locator: https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0；Fifth Edition ©2022，cheat
          sheet义项2
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-066aff06-6bef-4b2d-9870-f6ff7551db7f
    field: record
    value:
      id: tc-066aff06-6bef-4b2d-9870-f6ff7551db7f
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 将阅读、听闻或个人观察所得的摘录和笔记按选定标题组织起来的笔记本。
        basis:
        - entity: stern-fragment-whole
          locator: Tiffany Stern正文6–8段，L133–138
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-a922627b-3c76-4142-ad1b-b0b38c1bab3c
          text: commonplace book
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: stern-fragment-whole
            locator: Tiffany Stern正文6–8段，L133–138
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-e7af64e3-ac9e-4fbd-baaa-fecf3782cc5a
          text: 札记簿
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 札记簿为原中文登记，在此按主题标题组织摘录和观察的明确范围沿用；没有更强中文证据，不为换取文路径强制改为摘录簿。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: stern-fragment-whole
        locator: Tiffany Stern正文6–8段，L133–138
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-b49a8de0-d20e-42da-b7f0-f8d09ce44dc2
    field: record
    value:
      id: tc-b49a8de0-d20e-42da-b7f0-f8d09ce44dc2
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 修订版教育目标分类中区分记忆、理解、应用、分析、评价和创造的认知过程维度。
        basis:
        - entity: krathwohl-2002-taxonomy
          locator: PDFindex2–5/印刷pp.214–217，Cognitive Process dimension及Tables2–3
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-5877c07e-3cae-4a9e-9e48-d91b2ed09416
          text: cognitive process dimension
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: krathwohl-2002-taxonomy
            locator: PDFindex2–5/印刷pp.214–217，Cognitive Process dimension及Tables2–3
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-164f05a0-6ba3-447f-8cd9-2f1e9bf71bb3
          text: 认知过程维度
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 认知过程维度准确对应原条目本意引用的修订版分类，不泛称理解深度；知识维度另有其义，不合并。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: krathwohl-2002-taxonomy
        locator: PDFindex2–5/印刷pp.214–217，Cognitive Process dimension及Tables2–3
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-aadb304c-3ed0-4f60-94cf-c968953d838c
    field: record
    value:
      id: tc-aadb304c-3ed0-4f60-94cf-c968953d838c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 组织为实现其既定目的而被指导、监督并被问责的以人为本系统。
        basis:
        - entity: iso-37000-2021
          locator: §3.1.1，PDFp.9/印刷p.1
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-06b33584-8d3e-4053-ba8d-fb7658308c79
          text: governance of organizations
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-37000-2021
            locator: §3.1.1，PDFp.9/印刷p.1
            checked: '2026-09-06'
        - id: tm-37d5c3fd-96dc-4d05-9676-3e7955c10f52
          text: governance
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: iso-37000-2021
            locator: §3.1.1，PDFp.9/印刷p.1
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-fbdc1cb5-9e94-4eaf-ba39-857028742488
          text: 治理
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 治理保留组织层指导/监督/问责机制，不把对管理的管理概述当完整定义。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-37000-2021
        locator: §3.1.1，PDFp.9/印刷p.1
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-24c3f7b9-c6a2-4e1c-91f2-b3ee234219c8
    field: record
    value:
      id: tc-24c3f7b9-c6a2-4e1c-91f2-b3ee234219c8
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 治理主体正式表达的组织意向和方向。
        basis:
        - entity: iso-37000-2021
          locator: §3.2.9，PDFp.12/印刷p.4
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-acdb0fe2-bc90-41f2-90b0-079e9ea8d300
          text: governance policy
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-37000-2021
            locator: §3.2.9，PDFp.12/印刷p.4
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-54912589-583d-4140-88b2-e3d749a4c82f
          text: 治理政策
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 治理政策补足原行治理主体限定，源词头不是一般policy；旧必须遵守的规则概述与方向定义有实质差异，需明确采纳。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: iso-37000-2021
        locator: §3.2.9，PDFp.12/印刷p.4
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-e61924e8-88b7-4c88-aaf2-5dad229a89ed
    field: record
    value:
      id: tc-e61924e8-88b7-4c88-aaf2-5dad229a89ed
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 被赋予对特定事项作出决定的权限，明确哪些主体能在何种范围与条件下作出哪些决定。
        basis:
        - entity: dnd-caf-data-governance
          locator: 2022-07-28独立发表版；AppendixB data governance定义；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-bf128cba-2cb0-4d40-ae87-74222efdc371
          text: decision rights
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: dnd-caf-data-governance
            locator: 2022-07-28独立发表版；AppendixB data governance定义；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-641a6f25-0b53-4451-9834-f0d3ea1ce134
          text: 决策权
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 决策权是作决定的权限，区别执行职责和结果问责；DND具体主体与事项提供概念对应，不冒称DAMA付费原典。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: dnd-caf-data-governance
        locator: 2022-07-28独立发表版；AppendixB data governance定义；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-09ff3cd6-f825-4e90-b401-4ef25c2cc084
    field: record
    value:
      id: tc-09ff3cd6-f825-4e90-b401-4ef25c2cc084
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 持续、系统地收集或整理指定指标及其他资料，以掌握实施进展、结果和相关背景的过程。
        basis:
        - entity: oecd-2024-evaluation-glossary-en-zh
          locator: Monitoring，PDFp.39，官方英文/中文对应
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-d7c39844-82c4-4c45-ba9c-9902f7b17f51
          text: monitoring
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: oecd-2024-evaluation-glossary-en-zh
            locator: Monitoring，PDFp.39，官方英文/中文对应
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-cde84c16-a9a4-47fc-8ac3-205a5d51f1cc
          text: 监测
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: oecd-2024-evaluation-glossary-en-zh
            locator: Monitoring，PDFp.39，官方英文/中文对应
            checked: '2026-09-06'
      basis:
      - entity: oecd-2024-evaluation-glossary-en-zh
        locator: Monitoring，PDFp.39，官方英文/中文对应
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-f881797d-c9ff-4f57-9523-b6a1c01c8b2c
    field: record
    value:
      id: tc-f881797d-c9ff-4f57-9523-b6a1c01c8b2c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 对计划中、进行中或已完成的干预及其设计、实施和结果进行系统、客观评价的过程。
        basis:
        - entity: oecd-2024-evaluation-glossary-en-zh
          locator: Evaluation，PDFp.29，官方英文/中文对应
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-6f0fed97-fada-4463-b83f-92193c721185
          text: evaluation
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: oecd-2024-evaluation-glossary-en-zh
            locator: Evaluation，PDFp.29，官方英文/中文对应
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-deb24ad5-acf0-4260-b259-4c50c19bca4c
          text: 评估
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: oecd-2024-evaluation-glossary-en-zh
            locator: Evaluation，PDFp.29，官方英文/中文对应
            checked: '2026-09-06'
      basis:
      - entity: oecd-2024-evaluation-glossary-en-zh
        locator: Evaluation，PDFp.29，官方英文/中文对应
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-36a1e0f4-8fe1-459a-9083-b31022a1bda1
    field: record
    value:
      id: tc-36a1e0f4-8fe1-459a-9083-b31022a1bda1
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 在安全相关事务中，按时间顺序记录活动，使特定操作、过程或事件从开始到结果的活动序列能够被重建和检查的记录。
        basis:
        - entity: nist-sp-800-53r5
          locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；PDFp.422，AppendixA印刷p.395，audit
            trail
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-f3f51b2d-e126-4c4a-a2d5-3e621f5070f5
          text: audit trail
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: nist-sp-800-53r5
            locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；PDFp.422，AppendixA印刷p.395，audit
              trail
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-28bdb398-c344-489c-acef-a642f04ae4d2
          text: 审计追踪
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 审计追踪强调可重建的连续活动记录；谁/何时/何事可作为实现字段，不是全部定义。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: nist-sp-800-53r5
        locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；PDFp.422，AppendixA印刷p.395，audit
          trail
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-9ebb317b-d01a-4852-a71f-463f595a50a4
    field: record
    value:
      id: tc-9ebb317b-d01a-4852-a71f-463f595a50a4
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 对治理安排及其有效性的评审。
        basis:
        - entity: dfe-external-governance-reviews
          locator: 2026-08-11更新发表版；Benefits of an external governance review；Scope of the review
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-73cdf874-2e2b-4404-9eaf-6d0b71d41d0b
          text: governance review
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: dfe-external-governance-reviews
            locator: 2026-08-11更新发表版；Benefits of an external governance review；Scope of the review
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-f2c73c67-527c-442e-b5a7-882795cce1fc
          text: 治理评审
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 治理评审有官方实际用法；本库年度复审政策/决策权/阈值为项目实施规则，不冒称ISO37000有独立词条。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: dfe-external-governance-reviews
        locator: 2026-08-11更新发表版；Benefits of an external governance review；Scope of the review
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-ec453431-dede-440d-87aa-40b745fea33a
    field: record
    value:
      id: tc-ec453431-dede-440d-87aa-40b745fea33a
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 对记录和活动进行独立审查与检查，以评价系统控制的充分性，并确认是否符合既定政策和操作程序。
        basis:
        - entity: nist-sp-800-53r5
          locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；PDFp.422，AppendixA印刷p.395，audit
            [CNSSI4009]
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-4794e766-7ce2-4386-8b90-0c7ea06ce27a
          text: audit
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: nist-sp-800-53r5
            locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；PDFp.422，AppendixA印刷p.395，audit
              [CNSSI4009]
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-37aeadd2-d0a1-4a1f-9845-d3ba5b6b2b45
          text: 审计
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 审计与审计追踪不同，前者是评价过程，后者是记录；原符合规则概述补足证据和准则机制。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: nist-sp-800-53r5
        locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；PDFp.422，AppendixA印刷p.395，audit
          [CNSSI4009]
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-9db2bd8b-938e-4752-865f-bec2da9c4083
    field: record
    value:
      id: tc-9db2bd8b-938e-4752-865f-bec2da9c4083
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 本库中由人作出判断、而不是直接抄自来源的字段值。
        basis:
          project:
            approval: decision-term-data-values
            origin:
              commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
              file: docs/design/governance/maintenance.md
              locator: 断言
            rationale: 既有本库人工赋值用法；PROV-O只支持溯源，不冒充此定义来源
      languages:
      - language: en
        terms:
        - id: tm-657b1a85-79d5-44c1-b355-f37b4e7aff07
          text: assertion
          administrative_status: preferredTerm-admn-sts
          basis:
            project:
              approval: decision-term-data-values
              origin:
                commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
                file: docs/glossary.md
                locator: 治理与维护，断言/assertion原登记
              rationale: 仅此既有英文形式的项目准入追溯；不是模型英文兜底
      - language: zh-Hans
        terms:
        - id: tm-25528895-b7ab-4c59-b885-003d51cdf632
          text: 断言
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 断言在本条是本库限定用法，保留原名称，不扩大到所有命题断言。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
        project:
          approval: decision-term-data-values
          origin:
            commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
            file: docs/design/governance/maintenance.md
            locator: 断言
          rationale: 既有本库人工赋值用法；PROV-O只支持溯源，不冒充此定义来源
      workflow: active
  - identity: terms/concepts/tc-0aa7aa33-d7af-4c82-ad56-6efe59c4138c
    field: record
    value:
      id: tc-0aa7aa33-d7af-4c82-ad56-6efe59c4138c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 与干预及其结果或发生背景有关的定量或定性因素、变量。
        basis:
        - entity: oecd-2024-evaluation-glossary-en-zh
          locator: Indicator，PDFp.35，英文及官方中文指标紧邻
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-e36008bf-48ec-4391-991d-e4dc25d973e5
          text: indicator
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: oecd-2024-evaluation-glossary-en-zh
            locator: Indicator，PDFp.35，英文及官方中文指标紧邻
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-e81a6d8c-836b-4599-9dd9-6487df397223
          text: 指标
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: oecd-2024-evaluation-glossary-en-zh
            locator: Indicator，PDFp.35，英文及官方中文指标紧邻
            checked: '2026-09-06'
      basis:
      - entity: oecd-2024-evaluation-glossary-en-zh
        locator: Indicator，PDFp.35，英文及官方中文指标紧邻
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-549c1bed-5db4-4073-aaab-bf23c9be47ac
    field: record
    value:
      id: tc-549c1bed-5db4-4073-aaab-bf23c9be47ac
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用于判定指标何时触发复核或提案的界值。
        basis:
          project:
            approval: decision-term-data-values
            origin:
              commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
              file: docs/design/governance/maintenance.md
              locator: 阈值；触发与动作
            rationale: 现行阈值触发复核或提案，不自动批准修改
      languages:
      - language: en
        terms:
        - id: tm-1facfe30-6843-4a4a-989d-a7d8338cf57f
          text: threshold
          administrative_status: preferredTerm-admn-sts
          basis:
            project:
              approval: decision-term-data-values
              origin:
                commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
                file: docs/glossary.md
                locator: 治理与维护，阈值/threshold原登记
              rationale: 仅此既有英文形式的项目登记追溯
      - language: zh-Hans
        terms:
        - id: tm-f998c038-aacd-4c65-84df-c55042284579
          text: 阈值
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 阈值保留既有指标界值用法，明确到达阈值不授予自动修改权限。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
        project:
          approval: decision-term-data-values
          origin:
            commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
            file: docs/design/governance/maintenance.md
            locator: 阈值；触发与动作
          rationale: 现行阈值触发复核或提案，不自动批准修改
      workflow: active
  - identity: terms/concepts/tc-ab1c42d3-59d8-49db-9aa9-eebc09a98d6c
    field: record
    value:
      id: tc-ab1c42d3-59d8-49db-9aa9-eebc09a98d6c
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 完成接受程序并允许候选词作为词纳入受控词表的操作。
        basis:
        - entity: z39-19
          locator: §11.1.6 Candidate Terms，PDFp.105/印刷p.94；§11.4.5
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-def01f3e-50b7-4676-a941-bdda43a2dc21
          text: approve
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: z39-19
            locator: §11.1.6 Candidate Terms，PDFp.105/印刷p.94；§11.4.5
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-0abd2dc1-3755-4169-9f04-dfa271540391
          text: 批准
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 批准在此是源实际approved动词语境的接受动作，不伪造独立定义号，也不从标准授予本库机器审批权。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: z39-19
        locator: §11.1.6 Candidate Terms，PDFp.105/印刷p.94；§11.4.5
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-4aa4867f-ea92-4a56-a56f-e8ffe45c1f91
    field: record
    value:
      id: tc-4aa4867f-ea92-4a56-a56f-e8ffe45c1f91
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 知识图谱所表示的实体之间的语义联系。
        basis:
        - entity: hogan-paper
          locator: arXivv6，PDFp.1 L68–88，nodes represent entities/edges represent relations
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-a3356e3f-f6c3-43bb-b088-fe607d15a8c7
          text: relation
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hogan-paper
            locator: arXivv6，PDFp.1 L68–88，nodes represent entities/edges represent relations
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-d5811399-5efc-4f04-bcf1-ccea4145a933
          text: 关系
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 关系是语义联系，不是其图表示边；原relation与edge拆开，不泛化RDF predicate身份。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hogan-paper
        locator: arXivv6，PDFp.1 L68–88，nodes represent entities/edges represent relations
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-95d07268-89f1-4c7f-86b0-98f60eeeef52
    field: record
    value:
      id: tc-95d07268-89f1-4c7f-86b0-98f60eeeef52
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 图中连接节点的结构；在知识图谱中可用来表示实体之间的关系。
        basis:
        - entity: hogan-paper
          locator: arXivv6，PDFp.4 L192–200 directed edge-labelled graphs
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-b99aaec5-5d0c-4f7e-9ead-e73294328226
          text: edge
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hogan-paper
            locator: arXivv6，PDFp.4 L192–200 directed edge-labelled graphs
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-28070939-fa29-4c92-bfdc-f96ba6758174
          text: 边
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 边是图连接的行业名称，原定义已出现该词；作为独立中文designation本包明确提出模型第5级，不谎称旧表已经独立登记。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hogan-paper
        locator: arXivv6，PDFp.4 L192–200 directed edge-labelled graphs
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-daa1c79a-56f0-4d62-a360-ddaa9b332d0f
    field: record
    value:
      id: tc-daa1c79a-56f0-4d62-a360-ddaa9b332d0f
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 知识图谱或数据模型的高层结构说明，可涉及类型、关系和约束。
        basis:
        - entity: hogan-paper
          locator: arXivv6，PDFp.1 L84–88 high-level structure
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-f46f87b7-417d-492b-b34f-9bcb2a74fcef
          text: schema
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hogan-paper
            locator: arXivv6，PDFp.1 L84–88 high-level structure
            checked: '2026-09-06'
        - id: tm-bfe84c3f-798d-441f-9306-ea6e990a168a
          text: Schema
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: hogan-paper
            locator: arXivv6，PDFp.1 L84–88 high-level structure
            checked: '2026-09-06'
      basis:
      - entity: hogan-paper
        locator: arXivv6，PDFp.1 L84–88 high-level structure
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-e0ddd60c-cecf-4652-8b9d-2234f194a7a1
    field: record
    value:
      id: tc-e0ddd60c-cecf-4652-8b9d-2234f194a7a1
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 依据已有知识及本体或规则所表达的条件，推导或判定进一步知识是否成立的过程。
        basis:
        - entity: hogan-paper
          locator: arXivv6，§4.3 Reasoning、§4.3.1 Rules，Table6/Figure22
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-e5a02701-e0ef-4995-99a9-67f4132da244
          text: reasoning
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hogan-paper
            locator: arXivv6，§4.3 Reasoning、§4.3.1 Rules，Table6/Figure22
            checked: '2026-09-06'
        - id: tm-8e2fa2f3-0729-4c4c-a8eb-bbc5df747e6e
          text: inference
          administrative_status: admittedTerm-admn-sts
          basis:
          - entity: w3c-rdf-semantics-2004
            locator: AppendixB Glossary (Informative)，Inference，L1282
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-ac9b494f-ac60-4b34-9f0c-c1deb91ad26d
          text: 推理
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 推理在此是规则或本体条件下的推导/蕴涵判定，可物化或查询重写，不必写入新边；不扩成全部归纳学习。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hogan-paper
        locator: arXivv6，§4.3 Reasoning、§4.3.1 Rules，Table6/Figure22
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-5c59be76-71b8-4e7e-8bd7-3763d8058473
    field: record
    value:
      id: tc-5c59be76-71b8-4e7e-8bd7-3763d8058473
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 允许为节点和边关联标签及属性—值对的图数据模型。
        basis:
        - entity: hogan-paper
          locator: arXivv6，PDFp.6 L277–328 property graphs
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-53e44f07-69b0-4040-8946-8098102fb3d1
          text: property graph
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: hogan-paper
            locator: arXivv6，PDFp.6 L277–328 property graphs
            checked: '2026-09-06'
      - language: zh-Hans
        terms:
        - id: tm-a6977c3d-9ff1-4b1b-803b-0b604a67dacd
          text: 属性图
          administrative_status: preferredTerm-admn-sts
          basis:
            level: 5
            model:
              name: gpt-6-astra
              date: '2026-09-06'
              rationale: 属性图保留原图模型概念；Hogan已核正文支持定义，不伪称ISO39075完整条款已读。；模型知识第5级，外部中文用法未核实。
              approval: decision-term-data-values
      basis:
      - entity: hogan-paper
        locator: arXivv6，PDFp.6 L277–328 property graphs
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-1141d95e-3a9c-4955-bb15-2e7ff25b4cf2
    field: record
    value:
      id: tc-1141d95e-3a9c-4955-bb15-2e7ff25b4cf2
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: 用于属性图的声明式查询语言。
        basis:
        - entity: francis-et-al-2018-cypher
          locator: SIGMOD18作者稿PDFp.3/论文p.1434，§2 The Cypher Language
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-7e361d24-7036-4df6-b1d1-89d2ae56c6d1
          text: Cypher
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: francis-et-al-2018-cypher
            locator: SIGMOD18作者稿PDFp.3/论文p.1434，§2 The Cypher Language
            checked: '2026-09-06'
      basis:
      - entity: francis-et-al-2018-cypher
        locator: SIGMOD18作者稿PDFp.3/论文p.1434，§2 The Cypher Language
        checked: '2026-09-06'
      workflow: active
  - identity: terms/concepts/tc-5a533328-0f05-496f-b0dd-0436c4ef63b0
    field: record
    value:
      id: tc-5a533328-0f05-496f-b0dd-0436c4ef63b0
      subject_fields: []
      definitions:
      - language: zh-Hans
        text: ISO/IEC39075:2024规定的属性图数据管理语言。
        basis:
        - entity: iso-39075-2024
          locator: 官方Abstract：规定用于property graphs的数据管理语言syntax与semantics；Edition1，2024-04
          checked: '2026-09-06'
      languages:
      - language: en
        terms:
        - id: tm-3b963620-d52f-49e0-9c5b-3e3d9f52bcd2
          text: GQL
          administrative_status: preferredTerm-admn-sts
          basis:
          - entity: iso-39075-2024
            locator: 官方Abstract：规定用于property graphs的数据管理语言syntax与semantics；Edition1，2024-04
            checked: '2026-09-06'
      basis:
      - entity: iso-39075-2024
        locator: 官方Abstract：规定用于property graphs的数据管理语言syntax与semantics；Edition1，2024-04
        checked: '2026-09-06'
      workflow: active
- question: Q02
  resolution: recommended
  patches:
  - identity: terms/terms/tm-67cf1d57-71a5-4e5a-8294-ca5d0a931222
    field: record
    value:
      concept: tc-6908a022-5a5a-43e0-b895-4414bba97169
      language: en
      id: tm-67cf1d57-71a5-4e5a-8294-ca5d0a931222
      text: controlled vocabulary
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.12；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-e92e1633-a6e8-4eaa-91cd-fc1abd2d7cd3
    field: record
    value:
      concept: tc-6908a022-5a5a-43e0-b895-4414bba97169
      language: zh-Hans
      id: tm-e92e1633-a6e8-4eaa-91cd-fc1abd2d7cd3
      text: 受控词表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 受控词表是信息组织领域对预定且受管理的词汇列表的通行表达；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-0cad325d-695d-4f83-a05a-9ba8cb422e8a
    field: record
    value:
      concept: tc-c960c1a6-3e65-4075-801a-876b1d3b2f57
      language: en
      id: tm-0cad325d-695d-4f83-a05a-9ba8cb422e8a
      text: concept
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.11；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-1c54182a-deb7-427a-8426-68bd35811502
    field: record
    value:
      concept: tc-c960c1a6-3e65-4075-801a-876b1d3b2f57
      language: zh-Hans
      id: tm-1c54182a-deb7-427a-8426-68bd35811502
      text: 概念
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 概念对应思维单元而非字符串，是术语学与知识组织的基本表达；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-6819b288-3cb6-4479-9516-e2a25acf1618
    field: record
    value:
      concept: tc-c1473abd-3fc6-4570-bf19-cbb27b944fc2
      language: en
      id: tm-6819b288-3cb6-4479-9516-e2a25acf1618
      text: preferred term
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.45；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-b13a05dd-249c-4d95-b82d-d575249ffd1f
    field: record
    value:
      concept: tc-c1473abd-3fc6-4570-bf19-cbb27b944fc2
      language: en
      id: tm-b13a05dd-249c-4d95-b82d-d575249ffd1f
      text: descriptor
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.45 preferred term / descriptor；免费样章印刷p.9，本次直接重读
        checked: '2026-09-06'
  - identity: terms/terms/tm-d7a0c93f-489a-4385-93ce-a934df56a82f
    field: record
    value:
      concept: tc-c1473abd-3fc6-4570-bf19-cbb27b944fc2
      language: zh-Hans
      id: tm-d7a0c93f-489a-4385-93ce-a934df56a82f
      text: 首选词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 首选词突出标引时优先采用的名称；旧并列叙词暂不凭逗号加入同义形式；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-b662786b-e53c-4ed0-9cc8-35346e4c6e20
    field: record
    value:
      concept: tc-c1473abd-3fc6-4570-bf19-cbb27b944fc2
      language: zh-Hans
      id: tm-b662786b-e53c-4ed0-9cc8-35346e4c6e20
      text: 叙词
      administrative_status: admittedTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 叙词是图书情报与叙词表实践中descriptor的既有中文名称；本条限定标引时代表概念的首选词，不泛指任意词；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-1996dfd0-ddc6-437f-808f-5ad8ff4f2b81
    field: record
    value:
      concept: tc-75fa8baa-d6ec-400e-b90f-5039371a2d57
      language: en
      id: tm-1996dfd0-ddc6-437f-808f-5ad8ff4f2b81
      text: non-preferred term
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.39；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-cd530576-f163-4651-b468-3dbf8af5f014
    field: record
    value:
      concept: tc-75fa8baa-d6ec-400e-b90f-5039371a2d57
      language: zh-Hans
      id: tm-cd530576-f163-4651-b468-3dbf8af5f014
      text: 非首选词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 非首选词与首选词形成名称使用地位的对照；非叙词保留原登记待独立判断；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-3866b74f-a77b-46e9-95bc-f4b16fefd182
    field: record
    value:
      concept: tc-75fa8baa-d6ec-400e-b90f-5039371a2d57
      language: zh-Hans
      id: tm-3866b74f-a77b-46e9-95bc-f4b16fefd182
      text: 非叙词
      administrative_status: admittedTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 非叙词对应ISO§2.39同时列出的non-descriptor，在此指不用作直接标引而提供入口的词；与非首选词同范围；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-de3b29f2-97c9-489a-be7a-0c77c1368e29
    field: record
    value:
      concept: tc-dc59744d-a530-44b7-9de8-77e2766710e7
      language: en
      id: tm-de3b29f2-97c9-489a-be7a-0c77c1368e29
      text: identifier
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.25；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-a596d0b5-6739-41d4-a914-5171aa299fb5
    field: record
    value:
      concept: tc-dc59744d-a530-44b7-9de8-77e2766710e7
      language: zh-Hans
      id: tm-a596d0b5-6739-41d4-a914-5171aa299fb5
      text: 标识符
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 标识符用于识别对象而非描述对象，译名保留识别语义；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-1192a98f-d6b3-44ee-a68f-d2c60cad8464
    field: record
    value:
      concept: tc-75e8012c-351f-4303-b8c0-523454b9b730
      language: zh-Hans
      id: tm-1192a98f-d6b3-44ee-a68f-d2c60cad8464
      text: 等价关系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 等价关系在此连接两个表示形式，不混作跨词表映射；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-649ce784-1d46-4f8a-8d77-b093d37b085a
    field: record
    value:
      concept: tc-278494cf-719c-43f9-b954-2a54c61e5c45
      language: zh-Hans
      id: tm-649ce784-1d46-4f8a-8d77-b093d37b085a
      text: 层级关系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 层级关系表示范围包含，保留与等价和相关关系的区别；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-97b3a73e-ff28-43f8-a01a-be24595a7b24
    field: record
    value:
      concept: tc-589f6145-5330-4773-b2dd-27eeeaa6bc84
      language: zh-Hans
      id: tm-97b3a73e-ff28-43f8-a01a-be24595a7b24
      text: 相关关系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 相关关系是叙词表中非层级的语义关联；RT 保留为关系符号；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-960f6e22-a8fe-426c-b6ea-7f92f697d188
    field: record
    value:
      concept: tc-1fa87658-bf07-4540-a863-a4e98a2fa888
      language: en
      id: tm-960f6e22-a8fe-426c-b6ea-7f92f697d188
      text: facet
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.20；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-7dbccdb3-ab81-4d56-95cc-7b55b1e3d83a
    field: record
    value:
      concept: tc-1fa87658-bf07-4540-a863-a4e98a2fa888
      language: zh-Hans
      id: tm-7dbccdb3-ab81-4d56-95cc-7b55b1e3d83a
      text: 分面
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 分面是分面分类法对共同固有类别分组的传统译名；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-b60105ff-8590-4f3e-82dd-41b3e6f9d933
    field: record
    value:
      concept: tc-99e3245e-2f51-45d0-ba40-800d645f7f1f
      language: en
      id: tm-b60105ff-8590-4f3e-82dd-41b3e6f9d933
      text: facet analysis
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.21；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-31f1451a-6a7e-4415-b0e4-02c445d722c9
    field: record
    value:
      concept: tc-99e3245e-2f51-45d0-ba40-800d645f7f1f
      language: zh-Hans
      id: tm-31f1451a-6a7e-4415-b0e4-02c445d722c9
      text: 分面分析
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 分面分析表示上述分析和分组方法，不是给文档加多个字段；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-e992d008-5b21-4068-891d-6a4bbd30561d
    field: record
    value:
      concept: tc-a5b2fb0f-5cea-4d47-8629-04694918cbf9
      language: en
      id: tm-e992d008-5b21-4068-891d-6a4bbd30561d
      text: characteristic of division
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.4；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-58a4412c-5306-4b39-99dc-ab139550b589
    field: record
    value:
      concept: tc-a5b2fb0f-5cea-4d47-8629-04694918cbf9
      language: zh-Hans
      id: tm-58a4412c-5306-4b39-99dc-ab139550b589
      text: 划分特征
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 划分特征突出同级细分所依据的属性，避免把属性值本身叫特征；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-cf8405c5-923a-4e3c-9ebc-fd08013905af
    field: record
    value:
      concept: tc-6e6f7a15-910d-483e-b06c-3e3938aed39b
      language: en
      id: tm-cf8405c5-923a-4e3c-9ebc-fd08013905af
      text: node label
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.38；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-3e5b4977-db0a-413a-8556-f8f4b34fd5bc
    field: record
    value:
      concept: tc-6e6f7a15-910d-483e-b06c-3e3938aed39b
      language: zh-Hans
      id: tm-3e5b4977-db0a-413a-8556-f8f4b34fd5bc
      text: 节点标签
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 节点标签在词表显示中说明排列，不是普通图节点的名称；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-d8924442-07c0-4937-b3d3-3b198a24d8aa
    field: record
    value:
      concept: tc-c09e918a-cc3f-423c-bbca-c40c6766ef28
      language: en
      id: tm-d8924442-07c0-4937-b3d3-3b198a24d8aa
      text: array
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.1；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-70716b70-18a1-43d7-829a-1f174ebfc953
    field: record
    value:
      concept: tc-c09e918a-cc3f-423c-bbca-c40c6766ef28
      language: zh-Hans
      id: tm-70716b70-18a1-43d7-829a-1f174ebfc953
      text: 数组
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 数组在此限于叙词表的一组兄弟概念，与程序存储数组同形但不同义；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-83940a42-c171-42dd-b8db-84d62d19f2c6
    field: record
    value:
      concept: tc-6ce2328c-e952-40b8-b7d5-fd8dd958d0b7
      language: en
      id: tm-83940a42-c171-42dd-b8db-84d62d19f2c6
      text: concept group
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.18；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-96cb412b-bb9d-4f29-93f4-4e1b9bac16c3
    field: record
    value:
      concept: tc-6ce2328c-e952-40b8-b7d5-fd8dd958d0b7
      language: zh-Hans
      id: tm-96cb412b-bb9d-4f29-93f4-4e1b9bac16c3
      text: 概念组
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 概念组直指按准则选出的概念集合；过宽的分组暂保留原登记；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-5627bc80-145c-48a0-ba62-f54c7ac3b83c
    field: record
    value:
      concept: tc-6ce2328c-e952-40b8-b7d5-fd8dd958d0b7
      language: zh-Hans
      id: tm-5627bc80-145c-48a0-ba62-f54c7ac3b83c
      text: 分组
      administrative_status: admittedTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 分组在中文可指动作或结果；本条严格指按准则选定的概念集合，作为概念组的简短称呼，不表示分组操作或任意数据集合；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-6936dadd-bd45-487a-b3e1-0ec61a2f7c64
    field: record
    value:
      concept: tc-c47ee168-3ad4-4489-bc26-1cc64f94407f
      language: en
      id: tm-6936dadd-bd45-487a-b3e1-0ec61a2f7c64
      text: name authority list
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.50；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-a92be9a9-8e86-4aac-931c-4a5072bb461a
    field: record
    value:
      concept: tc-c47ee168-3ad4-4489-bc26-1cc64f94407f
      language: zh-Hans
      id: tm-a92be9a9-8e86-4aac-931c-4a5072bb461a
      text: 名称规范表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 名称规范表是规范控制中对个体名称保持一致的名称列表表达；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-a570aee4-b8a3-4fa4-a3a4-1d40403444dc
    field: record
    value:
      concept: tc-405390d9-57dc-47ca-9317-0120d5aa86eb
      language: en
      id: tm-a570aee4-b8a3-4fa4-a3a4-1d40403444dc
      text: equivalence mapping
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.27；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-7d69db17-67ab-436d-9994-539c6702b0e0
    field: record
    value:
      concept: tc-405390d9-57dc-47ca-9317-0120d5aa86eb
      language: zh-Hans
      id: tm-7d69db17-67ab-436d-9994-539c6702b0e0
      text: 等价映射
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 等价映射限定跨词表的概念对应，与表内词的等价关系区分；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-63f76467-9cba-462a-bf20-40fa3ef63225
    field: record
    value:
      concept: tc-eb9e1973-6b39-47f1-8b3e-845798b14ba4
      language: en
      id: tm-63f76467-9cba-462a-bf20-40fa3ef63225
      text: differentiated mapping
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.23；继承 docs/references/iso-25964.md 已核定义表；第三方免费样本
        checked: '2026-08-29'
  - identity: terms/terms/tm-8812567a-6b12-4d95-a87c-363250e59b95
    field: record
    value:
      concept: tc-eb9e1973-6b39-47f1-8b3e-845798b14ba4
      language: zh-Hans
      id: tm-8812567a-6b12-4d95-a87c-363250e59b95
      text: 区分式映射
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 区分式映射表达区分映射类型与质量的既有中文名称，不引入新的程度类别；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-180f1491-60d9-4ad6-ba75-1ba53e68fc61
    field: record
    value:
      concept: tc-b544dcf4-e88e-4456-bb9e-824b74d7abc8
      language: en
      id: tm-180f1491-60d9-4ad6-ba75-1ba53e68fc61
      text: mapping
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.41；docs/references/iso-25964.md 已核定义表
        checked: '2026-08-29'
  - identity: terms/terms/tm-9be97554-ada5-484d-848e-8d07cda553e1
    field: record
    value:
      concept: tc-b544dcf4-e88e-4456-bb9e-824b74d7abc8
      language: zh-Hans
      id: tm-9be97554-ada5-484d-848e-8d07cda553e1
      text: 映射
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 映射是信息组织中表示不同词表概念对应关系的既有中文表达；本行严格限于 §3.41 关系产物，不引入过程义。外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-28740536-c0a9-499e-b167-e47449e37cff
    field: record
    value:
      concept: tc-c5f2ed53-7f7e-40a1-8c89-a07dac98107b
      language: en
      id: tm-28740536-c0a9-499e-b167-e47449e37cff
      text: synonym ring
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §5.4.2；PDF page index 28-29
        checked: '2026-09-06'
  - identity: terms/terms/tm-fc11144d-35cd-472b-a85d-23bc72f9e6c2
    field: record
    value:
      concept: tc-c5f2ed53-7f7e-40a1-8c89-a07dac98107b
      language: zh-Hans
      id: tm-fc11144d-35cd-472b-a85d-23bc72f9e6c2
      text: 同义词环
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 同义词环指检索时视为等价的一组词，名称突出检索扩展而非标引选词；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-3fbb53ad-04df-4f9d-b94f-58cecc7d80b8
    field: record
    value:
      concept: tc-c6190e59-1353-4f22-8a93-b3077b486884
      language: en
      id: tm-3fbb53ad-04df-4f9d-b94f-58cecc7d80b8
      text: taxonomy
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §5.4.3；PDF page index 29
        checked: '2026-09-06'
  - identity: terms/terms/tm-fc044200-56a9-4783-b4df-a6c1fc3f51e4
    field: record
    value:
      concept: tc-c6190e59-1353-4f22-8a93-b3077b486884
      language: zh-Hans
      id: tm-fc044200-56a9-4783-b4df-a6c1fc3f51e4
      text: 分类法
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 分类法是知识组织中 taxonomy 的既有行业译名；此处限于首选词的层级受控词表；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-baf0b11a-4d8a-415b-83d9-0f6d64662d6a
    field: record
    value:
      concept: tc-5c7a2951-c99c-4597-baa5-c6eb7fd7c5e4
      language: en
      id: tm-baf0b11a-4d8a-415b-83d9-0f6d64662d6a
      text: thesaurus
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §5.4.4；PDF page index 29
        checked: '2026-09-06'
  - identity: terms/terms/tm-8b27bf95-89c5-4e8b-a033-e0defb04a51c
    field: record
    value:
      concept: tc-5c7a2951-c99c-4597-baa5-c6eb7fd7c5e4
      language: zh-Hans
      id: tm-8b27bf95-89c5-4e8b-a033-e0defb04a51c
      text: 叙词表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 叙词表是信息检索领域对具有规范关系的受控词表的传统名称；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-d9b07ebb-8bba-4a1b-8b14-350fda733371
    field: record
    value:
      concept: tc-26a41c49-f435-4527-b419-de688657db90
      language: en
      id: tm-d9b07ebb-8bba-4a1b-8b14-350fda733371
      text: qualifier
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §4.1；§6.2.1；PDF page index 19；31-32
        checked: '2026-09-06'
  - identity: terms/terms/tm-d3e0ce32-0761-40d2-b0ca-4bf9dbf7a110
    field: record
    value:
      concept: tc-26a41c49-f435-4527-b419-de688657db90
      language: zh-Hans
      id: tm-d3e0ce32-0761-40d2-b0ca-4bf9dbf7a110
      text: 限定词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 限定词用于限制名称解释范围并区分同形异义；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-2b91ad37-5e29-4f00-90f7-6fc791205905
    field: record
    value:
      concept: tc-7f29a362-cc5b-481a-87df-67ff11c9c068
      language: en
      id: tm-2b91ad37-5e29-4f00-90f7-6fc791205905
      text: content object
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §4.1；§5.2.2；PDF page index 15；22-23
        checked: '2026-09-06'
  - identity: terms/terms/tm-26d027c7-af05-417b-a6b5-6c1523e04613
    field: record
    value:
      concept: tc-7f29a362-cc5b-481a-87df-67ff11c9c068
      language: zh-Hans
      id: tm-26d027c7-af05-417b-a6b5-6c1523e04613
      text: 内容对象
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 内容对象表明被组织和检索的对象，不自动等同本库内容单元；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-00cb8d21-abc0-4676-8a07-bafda70bd0cb
    field: record
    value:
      concept: tc-74b2becc-3bbe-45b5-8d42-bda67dcc17f8
      language: en
      id: tm-00cb8d21-abc0-4676-8a07-bafda70bd0cb
      text: scope note
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §4.1；§6.2.2；PDF page index 20；33
        checked: '2026-09-06'
  - identity: terms/terms/tm-a1591f11-abf4-440c-865b-2b448311b1c3
    field: record
    value:
      concept: tc-74b2becc-3bbe-45b5-8d42-bda67dcc17f8
      language: zh-Hans
      id: tm-a1591f11-abf4-440c-865b-2b448311b1c3
      text: 范围注释
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 范围注释说明名称采用的含义与使用边界；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-d6b7cf59-38bf-4400-a676-04b7e516cdc1
    field: record
    value:
      concept: tc-e7c36840-9dc5-45d1-a371-920c28af2a00
      language: en
      id: tm-d6b7cf59-38bf-4400-a676-04b7e516cdc1
      text: history note
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §4.1；§6.2.3；§11.3.2.2；PDF page index 19；33-34；108
        checked: '2026-09-06'
  - identity: terms/terms/tm-d1bad412-4998-412f-9e3a-0fdf3c1e3740
    field: record
    value:
      concept: tc-e7c36840-9dc5-45d1-a371-920c28af2a00
      language: zh-Hans
      id: tm-d1bad412-4998-412f-9e3a-0fdf3c1e3740
      text: 历史注释
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 历史注释记录术语的时间变化，与说明概念含义的范围注释区别；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-8ec912e8-3242-45f7-bf32-97bd40f61efe
    field: record
    value:
      concept: tc-155c651f-9cb6-4e89-b394-9b843b268148
      language: en
      id: tm-8ec912e8-3242-45f7-bf32-97bd40f61efe
      text: candidate term
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §4.1；§11.1.6；PDF page index 19；104
        checked: '2026-09-06'
  - identity: terms/terms/tm-e995203f-bdd8-4c79-8368-d199e049c0d2
    field: record
    value:
      concept: tc-155c651f-9cb6-4e89-b394-9b843b268148
      language: en
      id: tm-e995203f-bdd8-4c79-8368-d199e049c0d2
      text: provisional term
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §4.1；§11.1.6；PDF page index 19；104
        checked: '2026-09-06'
  - identity: terms/terms/tm-e7b7cd31-246e-4986-b5d3-d2fa7cb059b0
    field: record
    value:
      concept: tc-155c651f-9cb6-4e89-b394-9b843b268148
      language: zh-Hans
      id: tm-e7b7cd31-246e-4986-b5d3-d2fa7cb059b0
      text: 候选词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 候选词表示尚未完成收录审批的名称，而非来源实体状态；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-3f9dbaa9-c7b6-40d6-b4d1-8c83221df19b
    field: record
    value:
      concept: tc-a17e54a7-07e9-459e-86cc-bd0c12e4d58b
      language: en
      id: tm-3f9dbaa9-c7b6-40d6-b4d1-8c83221df19b
      text: unassigned term
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §11.1.8；PDF page index 104
        checked: '2026-09-06'
  - identity: terms/terms/tm-3d5a2c5e-8990-4a32-9a37-6a6b18d8f1e9
    field: record
    value:
      concept: tc-a17e54a7-07e9-459e-86cc-bd0c12e4d58b
      language: zh-Hans
      id: tm-3d5a2c5e-8990-4a32-9a37-6a6b18d8f1e9
      text: 未标引词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 未标引词强调尚未实际分配给内容对象，不表示禁止使用；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-4311cc75-0005-46aa-a296-0c6c9aa89900
    field: record
    value:
      concept: tc-88088c7a-5aaf-458c-a55c-23ff38463ee0
      language: en
      id: tm-4311cc75-0005-46aa-a296-0c6c9aa89900
      text: orphan term
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §4.1；§11.4.4；PDF page index 19；112
        checked: '2026-09-06'
  - identity: terms/terms/tm-d6b4f6d9-8e3f-4d8c-b418-79688e2cc5df
    field: record
    value:
      concept: tc-88088c7a-5aaf-458c-a55c-23ff38463ee0
      language: zh-Hans
      id: tm-d6b4f6d9-8e3f-4d8c-b418-79688e2cc5df
      text: 孤儿词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 孤儿词是缺乏层级和相关联系的词表维护用语；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-2bcd97cb-cdf8-4d28-b8ab-7e688f8d1d7e
    field: record
    value:
      concept: tc-6cb09f56-afea-40d2-a986-c0d80d376363
      language: en
      id: tm-2bcd97cb-cdf8-4d28-b8ab-7e688f8d1d7e
      text: literary warrant
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §5.3.5.1；PDF page index 27
        checked: '2026-09-06'
  - identity: terms/terms/tm-dfed1194-5cd6-48d1-8667-a5c47ebb30bb
    field: record
    value:
      concept: tc-6cb09f56-afea-40d2-a986-c0d80d376363
      language: zh-Hans
      id: tm-dfed1194-5cd6-48d1-8667-a5c47ebb30bb
      text: 文献依据
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 文献依据以领域文献中的实际使用作为收词理由；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-7046ee19-1db6-4df4-9664-aa85f07387fb
    field: record
    value:
      concept: tc-1ad36b83-83d4-4174-8cc0-a6189b8ce11b
      language: en
      id: tm-7046ee19-1db6-4df4-9664-aa85f07387fb
      text: organizational warrant
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §5.3.5.2；PDF page index 27
        checked: '2026-09-06'
  - identity: terms/terms/tm-b7475d7a-e888-4f21-ac57-b1801222311e
    field: record
    value:
      concept: tc-1ad36b83-83d4-4174-8cc0-a6189b8ce11b
      language: zh-Hans
      id: tm-b7475d7a-e888-4f21-ac57-b1801222311e
      text: 组织依据
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 组织依据突出采用组织偏好的名称形式；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-e4155133-bdc6-4af2-9231-29ac5963363d
    field: record
    value:
      concept: tc-60cd4ded-814a-46d1-9bd6-360f1b725ca0
      language: en
      id: tm-e4155133-bdc6-4af2-9231-29ac5963363d
      text: user warrant
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §5.3.5.3；PDF page index 27
        checked: '2026-09-06'
  - identity: terms/terms/tm-dcdba69e-639f-4ce6-b2ab-bea261846a7f
    field: record
    value:
      concept: tc-60cd4ded-814a-46d1-9bd6-360f1b725ca0
      language: zh-Hans
      id: tm-dcdba69e-639f-4ce6-b2ab-bea261846a7f
      text: 用户依据
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 用户依据反映检索用户实际使用的表达；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-1492b91e-ee09-46b6-b487-6d769897554e
    field: record
    value:
      concept: tc-60ca56e9-0bf5-4e06-86c4-b6941a9adc6e
      language: en
      id: tm-1492b91e-ee09-46b6-b487-6d769897554e
      text: vocabulary control
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §1.2；§4.1；PDF page index 12；21
        checked: '2026-09-06'
  - identity: terms/terms/tm-614c6eb9-c481-41b5-8374-d4be3d62b4d5
    field: record
    value:
      concept: tc-60ca56e9-0bf5-4e06-86c4-b6941a9adc6e
      language: zh-Hans
      id: tm-614c6eb9-c481-41b5-8374-d4be3d62b4d5
      text: 词汇控制
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 词汇控制是协调同义、异义和关系以使标引检索一致的行业表达；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-18e3b5c1-b6c5-4ddd-9b60-64435812ef57
    field: record
    value:
      concept: tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63
      language: en
      id: tm-18e3b5c1-b6c5-4ddd-9b60-64435812ef57
      text: list
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §5.4.1；印刷 p.17
        checked: '2026-09-06'
  - identity: terms/terms/tm-42bb0163-eaa8-4a85-9cbe-f4968c0dcd2d
    field: record
    value:
      concept: tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63
      language: en
      id: tm-42bb0163-eaa8-4a85-9cbe-f4968c0dcd2d
      text: pick list
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §5.4.1；印刷 p.17
        checked: '2026-09-06'
  - identity: terms/terms/tm-74a9e0b7-478f-48e1-9b61-00ca7b63bd12
    field: record
    value:
      concept: tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63
      language: zh-Hans
      id: tm-74a9e0b7-478f-48e1-9b61-00ca7b63bd12
      text: 列表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 列表是有限术语按明确顺序排列这一既有概念的行业表达；避免把glossary或code list的专门名称作为无条件同义词；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-486daf92-5ede-4f80-a324-75c113c41708
    field: record
    value:
      concept: tc-ddf950fe-a885-4424-82f9-cfbb5d4ab330
      language: en
      id: tm-486daf92-5ede-4f80-a324-75c113c41708
      text: top down
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json
        checked: '2026-09-06'
  - identity: terms/terms/tm-713d5d4c-9326-478f-8e94-b0e5f690c812
    field: record
    value:
      concept: tc-ddf950fe-a885-4424-82f9-cfbb5d4ab330
      language: zh-Hans
      id: tm-713d5d4c-9326-478f-8e94-b0e5f690c812
      text: 自上而下
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 自上而下保留从宽到窄的词表建设方向；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-7bf170bd-f546-4f38-aa43-51e301cc2976
    field: record
    value:
      concept: tc-6f960f39-1a53-4215-932e-a89f837ac06c
      language: en
      id: tm-7bf170bd-f546-4f38-aa43-51e301cc2976
      text: bottom up
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §11.1.3.1；work/reviews/2026-09-06-term-niso-evidence.json
        checked: '2026-09-06'
  - identity: terms/terms/tm-a3a9225d-75eb-41bb-b912-c8b01a442062
    field: record
    value:
      concept: tc-6f960f39-1a53-4215-932e-a89f837ac06c
      language: zh-Hans
      id: tm-a3a9225d-75eb-41bb-b912-c8b01a442062
      text: 自下而上
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 自下而上保留从具体语料词向一般词组织的方向；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-fc3bf25c-4cd0-4393-9aca-20543b39de42
    field: record
    value:
      concept: tc-208354ed-1338-4152-be98-ca93504c3355
      language: en
      id: tm-fc3bf25c-4cd0-4393-9aca-20543b39de42
      text: deductive
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json
        checked: '2026-09-06'
  - identity: terms/terms/tm-3f18476e-cd74-4c14-a5d1-94361a9c6bc8
    field: record
    value:
      concept: tc-208354ed-1338-4152-be98-ca93504c3355
      language: zh-Hans
      id: tm-3f18476e-cd74-4c14-a5d1-94361a9c6bc8
      text: 演绎法
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 演绎法在此是 NISO 词表建设方法的既有表达，不外推到逻辑学推理定义；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-bd7ee62c-43b5-4878-8023-dfdfc68f03d2
    field: record
    value:
      concept: tc-c9b65491-09a6-4765-b208-6601af494f31
      language: en
      id: tm-bd7ee62c-43b5-4878-8023-dfdfc68f03d2
      text: inductive
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §11.1.3.2；work/reviews/2026-09-06-term-niso-evidence.json
        checked: '2026-09-06'
  - identity: terms/terms/tm-31f1c425-6625-40c3-9f7d-a23b93e495fe
    field: record
    value:
      concept: tc-c9b65491-09a6-4765-b208-6601af494f31
      language: zh-Hans
      id: tm-31f1c425-6625-40c3-9f7d-a23b93e495fe
      text: 归纳法
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 归纳法在此突出从一开始控制和逐项组织词汇，不与普通逻辑学定义混同；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-35a8bfd4-703e-41ec-bb76-9b05e048608c
    field: record
    value:
      concept: tc-dfe493d2-f173-4a9e-ace9-b9ffad3f0f0f
      language: en
      id: tm-35a8bfd4-703e-41ec-bb76-9b05e048608c
      text: recall
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 947-955
        checked: '2026-09-06'
  - identity: terms/terms/tm-119ca7ee-aa9d-4d04-b352-b214e2ea3962
    field: record
    value:
      concept: tc-dfe493d2-f173-4a9e-ace9-b9ffad3f0f0f
      language: zh-Hans
      id: tm-119ca7ee-aa9d-4d04-b352-b214e2ea3962
      text: 查全率
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 查全率是信息检索中对全部相关对象检出程度的行业名称；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-9962ad11-5853-4ed6-aa79-43335bb9aa59
    field: record
    value:
      concept: tc-11e8d232-85f8-4e00-98a0-d8bdd7adf639
      language: en
      id: tm-9962ad11-5853-4ed6-aa79-43335bb9aa59
      text: precision
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: PDF page index 19（第 20 页，印刷 p. 8-9），glossary, extracted lines 918-926
        checked: '2026-09-06'
  - identity: terms/terms/tm-bd0ee821-6214-4efe-8771-67403605f612
    field: record
    value:
      concept: tc-11e8d232-85f8-4e00-98a0-d8bdd7adf639
      language: zh-Hans
      id: tm-bd0ee821-6214-4efe-8771-67403605f612
      text: 查准率
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 查准率是信息检索中对检出结果相关程度的行业名称；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-3f32ff2e-2739-4982-9971-ff06c324a402
    field: record
    value:
      concept: tc-9d793546-528c-4b51-8a37-801df07342f3
      language: en
      id: tm-3f32ff2e-2739-4982-9971-ff06c324a402
      text: ontology
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: gruber-official
        locator: L14-L24；英文形式 ontology；作者定义为 explicit specification of a conceptualization；代表原语包括 classes、attributes、relationships
          及其约束（L15-L16）
        checked: '2026-09-06'
  - identity: terms/terms/tm-f1d2d279-3d8f-4f39-b490-8f0c211d15b9
    field: record
    value:
      concept: tc-9d793546-528c-4b51-8a37-801df07342f3
      language: zh-Hans
      id: tm-f1d2d279-3d8f-4f39-b490-8f0c211d15b9
      text: 本体
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 本体是知识表示领域 ontology 的通行译名，限于概念化规范；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-2d4a0c3e-052f-4110-b3c6-9f08982cbb34
    field: record
    value:
      concept: tc-c7d6f1d5-2139-4d42-857d-7c16fa507b31
      language: en
      id: tm-2d4a0c3e-052f-4110-b3c6-9f08982cbb34
      text: knowledge graph
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hogan-paper
        locator: P1 L68-L89；P6 L277-L328；P1 L71-L83 直接支持现实世界知识、实体节点、实体间关系、图数据模型及可用本体/规则表达量化知识
        checked: '2026-09-06'
  - identity: terms/terms/tm-60f284eb-71a8-490b-be2a-b6fabcb92d8b
    field: record
    value:
      concept: tc-c7d6f1d5-2139-4d42-857d-7c16fa507b31
      language: zh-Hans
      id: tm-60f284eb-71a8-490b-be2a-b6fabcb92d8b
      text: 知识图谱
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 知识图谱表述以图积累和传达知识的数据组织；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-94cd7a7d-4b17-4493-968d-12bdee0c0bb7
    field: record
    value:
      concept: tc-99ace251-fdee-4ab9-93e8-a016e7e98127
      language: en
      id: tm-94cd7a7d-4b17-4493-968d-12bdee0c0bb7
      text: DCMI Metadata Terms
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: dcmi-metadata-terms
        locator: §1；DCMIType 条目；dc:type 条目；DCMI Metadata Terms 包含 properties、classes、datatypes、vocabulary encoding schemes；不是只有属性与类
        checked: '2026-09-06'
  - identity: terms/terms/tm-f04583f9-f962-4c1f-bf3e-8cf3748b4205
    field: record
    value:
      concept: tc-3f06d868-d7d2-4612-ad2b-35614912ba40
      language: en
      id: tm-f04583f9-f962-4c1f-bf3e-8cf3748b4205
      text: DCMI Type Vocabulary
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: dcmi-metadata-terms
        locator: §1；DCMIType 条目；dc:type 条目；DCMI 官方将 DCMIType 定义为用于分类资源性质或体裁的类集合；`dcterms:type` 建议使用受控词表
        checked: '2026-09-06'
  - identity: terms/terms/tm-eecf3ffd-6446-4574-966d-09a7304e8a7c
    field: record
    value:
      concept: tc-589ad410-5fc7-4f1b-ba5a-fd06c366016f
      language: en
      id: tm-eecf3ffd-6446-4574-966d-09a7304e8a7c
      text: triple
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: rdf11
        locator: §3.1 Triples；RDF triple 的 subject、predicate、object 三组件；顺序为 subject-predicate-object
        checked: '2026-09-06'
  - identity: terms/terms/tm-9fdaa528-7ee8-4a29-ae7f-a8b08aaa0380
    field: record
    value:
      concept: tc-589ad410-5fc7-4f1b-ba5a-fd06c366016f
      language: zh-Hans
      id: tm-9fdaa528-7ee8-4a29-ae7f-a8b08aaa0380
      text: 三元组
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 三元组在 RDF 中明确对应主语、谓语、宾语三组件；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-be311ab7-f917-4c29-840c-2ef0e64c23cf
    field: record
    value:
      concept: tc-e638bec2-4c85-4eed-9721-8175f5417f6d
      language: en
      id: tm-be311ab7-f917-4c29-840c-2ef0e64c23cf
      text: SPARQL
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: sparql11
        locator: §1 Introduction；SPARQL 1.1 规范定义 RDF 查询语言的 syntax 和 semantics
        checked: '2026-09-06'
  - identity: terms/terms/tm-ceea4cbc-ecb1-4aa5-9d44-82267d0d943c
    field: record
    value:
      concept: tc-acd244b6-0d82-4366-ac25-3fb7260c6473
      language: en
      id: tm-ceea4cbc-ecb1-4aa5-9d44-82267d0d943c
      text: Resource Description Framework
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: rdf11
        locator: Introduction；§3.1 Triples
        checked: '2026-09-06'
  - identity: terms/terms/tm-4e708f52-6a2a-4ae6-b9cb-b7286d3a85d0
    field: record
    value:
      concept: tc-acd244b6-0d82-4366-ac25-3fb7260c6473
      language: en
      id: tm-4e708f52-6a2a-4ae6-b9cb-b7286d3a85d0
      text: RDF
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: rdf11
        locator: Introduction；§3.1 Triples
        checked: '2026-09-06'
  - identity: terms/terms/tm-7019ad5a-e9f6-4db3-8596-3e29c256455c
    field: record
    value:
      concept: tc-2633b390-938e-4c0b-9bec-deebf8f65e8b
      language: en
      id: tm-7019ad5a-e9f6-4db3-8596-3e29c256455c
      text: Simple Knowledge Organization System
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: skos
        locator: Introduction；SKOS data model
        checked: '2026-09-06'
  - identity: terms/terms/tm-e854dfc3-779a-4e51-8253-520cc3722fec
    field: record
    value:
      concept: tc-2633b390-938e-4c0b-9bec-deebf8f65e8b
      language: en
      id: tm-e854dfc3-779a-4e51-8253-520cc3722fec
      text: SKOS
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: skos
        locator: Introduction；SKOS data model
        checked: '2026-09-06'
  - identity: terms/terms/tm-b710284d-ad1f-47d2-911d-616d0aba7688
    field: record
    value:
      concept: tc-a07a37d8-13b6-4a9d-b86c-ba96f0c080b4
      language: en
      id: tm-b710284d-ad1f-47d2-911d-616d0aba7688
      text: RDFS
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: rdfs11
        locator: Abstract；§1
        checked: '2026-09-06'
  - identity: terms/terms/tm-e587b46e-66cd-43a1-8423-339602565de7
    field: record
    value:
      concept: tc-b4f8bca4-b3cf-405b-8cf1-ea45112783d2
      language: en
      id: tm-e587b46e-66cd-43a1-8423-339602565de7
      text: OWL
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: owl2
        locator: Abstract；§1
        checked: '2026-09-06'
  - identity: terms/terms/tm-e35cfb69-400f-4114-925b-5b139615c090
    field: record
    value:
      concept: tc-cb8ba91f-0bce-4b3d-ac6a-26bfca9ab7c9
      language: en
      id: tm-e35cfb69-400f-4114-925b-5b139615c090
      text: Application Profile
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: dcmi-singapore-framework
        locator: §3.1–3.3；docs/references/dcmi-application-profiles.md 已核阅读范围
        checked: '2026-09-01'
  - identity: terms/terms/tm-849f1000-68b5-456c-954f-1b05750ebea3
    field: record
    value:
      concept: tc-224b9f45-d624-4543-bc81-f64d02f81aa0
      language: en
      id: tm-849f1000-68b5-456c-954f-1b05750ebea3
      text: Reproducible Builds
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: lamb-zacchiroli-2021-reproducible-builds
        locator: https://arxiv.org/pdf/2104.06020v1；PDF p. 2，Reproducible Builds，Definition 1
        checked: '2026-09-06'
  - identity: terms/terms/tm-76611867-5bf8-4ba7-91b8-98328562a9aa
    field: record
    value:
      concept: tc-2cdb43fb-ad5e-4aec-ad71-56eb596b78eb
      language: en
      id: tm-76611867-5bf8-4ba7-91b8-98328562a9aa
      text: relevant
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-24495-1
        locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 1；PDF pp. 9–11（印刷 pp. 3–5），§5.1.1–§5.1.6
        checked: '2026-09-06'
  - identity: terms/terms/tm-e1b3aa8a-c184-4ee7-a2bd-0f9cacb93187
    field: record
    value:
      concept: tc-2cdb43fb-ad5e-4aec-ad71-56eb596b78eb
      language: zh-Hans
      id: tm-e1b3aa8a-c184-4ee7-a2bd-0f9cacb93187
      text: 相关
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 相关强调内容符合读者当前信息需要；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-aeb4615f-2f52-4dfd-a5e9-380a05c4e374
    field: record
    value:
      concept: tc-2938e52c-9172-4bc1-b3ea-a1c0476fe909
      language: en
      id: tm-aeb4615f-2f52-4dfd-a5e9-380a05c4e374
      text: findable
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-24495-1
        locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 2；PDF p. 11（印刷 p. 5），§5.2.1–§5.2.3
        checked: '2026-09-06'
  - identity: terms/terms/tm-290bf765-6c24-4495-9a46-ebe1e7fe462a
    field: record
    value:
      concept: tc-2938e52c-9172-4bc1-b3ea-a1c0476fe909
      language: zh-Hans
      id: tm-290bf765-6c24-4495-9a46-ebe1e7fe462a
      text: 可找到
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 可找到强调结构和设计支持定位信息；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-71fd160f-eff7-42b2-898f-4c56dd08230d
    field: record
    value:
      concept: tc-973e68b6-1e0f-47a9-9ab7-0660d591969c
      language: en
      id: tm-71fd160f-eff7-42b2-898f-4c56dd08230d
      text: understandable
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-24495-1
        locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 3
        checked: '2026-09-06'
  - identity: terms/terms/tm-8da4cfa3-6bcd-4bbb-84e8-e36f3db0e01f
    field: record
    value:
      concept: tc-973e68b6-1e0f-47a9-9ab7-0660d591969c
      language: zh-Hans
      id: tm-8da4cfa3-6bcd-4bbb-84e8-e36f3db0e01f
      text: 可理解
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 可理解强调读者对所找到信息的理解；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-73551363-0781-49db-b2fb-ae329c7ed476
    field: record
    value:
      concept: tc-9985f5e9-89cc-4fe1-849f-c2be99f97727
      language: en
      id: tm-73551363-0781-49db-b2fb-ae329c7ed476
      text: usable
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-24495-1
        locator: ISO 24495-1:2023 免费样章 PDF p. 9（印刷 p. 3），§4 Principle 4 及原则关系段
        checked: '2026-09-06'
  - identity: terms/terms/tm-d3c0e7d5-190f-4e6a-9b6b-4b395590ed75
    field: record
    value:
      concept: tc-9985f5e9-89cc-4fe1-849f-c2be99f97727
      language: zh-Hans
      id: tm-d3c0e7d5-190f-4e6a-9b6b-4b395590ed75
      text: 可使用
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 可使用强调信息支持读者完成预期任务；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-021f20e2-f065-4e09-ba80-2542f94f0c17
    field: record
    value:
      concept: tc-e5c11065-dc49-4ac8-b297-aadb2edd1196
      language: en
      id: tm-021f20e2-f065-4e09-ba80-2542f94f0c17
      text: fleeting note
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: ahrens-zettelkasten-interview
        locator: https://examstudyexpert.com/zettelkasten/ ; captured L91-L95
        checked: '2026-09-06'
  - identity: terms/terms/tm-01f3402c-0616-4c48-8bd4-e959046120d2
    field: record
    value:
      concept: tc-e5c11065-dc49-4ac8-b297-aadb2edd1196
      language: zh-Hans
      id: tm-01f3402c-0616-4c48-8bd4-e959046120d2
      text: 闪念笔记
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 闪念笔记强调临时想法提醒与后续处理；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-34df14ea-ab98-4b85-a833-9d7d06773428
    field: record
    value:
      concept: tc-80512a5e-8cde-40f7-8abe-896d973ee851
      language: en
      id: tm-34df14ea-ab98-4b85-a833-9d7d06773428
      text: literature note
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: ahrens-zettelkasten-interview
        locator: https://examstudyexpert.com/zettelkasten/ ; captured L103-L106
        checked: '2026-09-06'
  - identity: terms/terms/tm-494f248e-2538-4d16-ac58-ff1d43102dc3
    field: record
    value:
      concept: tc-80512a5e-8cde-40f7-8abe-896d973ee851
      language: zh-Hans
      id: tm-494f248e-2538-4d16-ac58-ff1d43102dc3
      text: 文献笔记
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 文献笔记强调针对阅读材料而作，不等同复制摘录；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-fdbe3135-7fb4-423f-bcbc-8376810130d5
    field: record
    value:
      concept: tc-5a5c6042-effa-4ebe-8a85-4560468e3adc
      language: en
      id: tm-fdbe3135-7fb4-423f-bcbc-8376810130d5
      text: permanent note
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: ahrens-zettelkasten-interview
        locator: https://examstudyexpert.com/zettelkasten/ ; captured L95-L102；https://examstudyexpert.com/zettelkasten/ ;
          captured L113-L114
        checked: '2026-09-06'
  - identity: terms/terms/tm-3d623e69-aa38-46cc-874b-506af3f67671
    field: record
    value:
      concept: tc-5a5c6042-effa-4ebe-8a85-4560468e3adc
      language: zh-Hans
      id: tm-3d623e69-aa38-46cc-874b-506af3f67671
      text: 永久笔记
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 永久笔记强调经过处理并长期连接发展的笔记；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-55036694-aa11-45ee-9c54-73f98f209ffd
    field: record
    value:
      concept: tc-362abd86-fd94-42b4-8f6e-aaca8aa3660b
      language: en
      id: tm-55036694-aa11-45ee-9c54-73f98f209ffd
      text: disposition
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-15489-1
        locator: https://cdn.standards.iteh.ai/samples/62542/fe383f4fe10448d5b22ce628b1542ed6/ISO-15489-1-2016.pdf；PDF p.
          10（印刷 p. 2），§3.8 disposition
        checked: '2026-09-06'
  - identity: terms/terms/tm-47d9bbbe-00da-47da-bb2f-738a62d9bfce
    field: record
    value:
      concept: tc-362abd86-fd94-42b4-8f6e-aaca8aa3660b
      language: zh-Hans
      id: tm-47d9bbbe-00da-47da-bb2f-738a62d9bfce
      text: 处置
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 处置是文件管理中对保管、销毁或移交决定的执行，不等于删除；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-75b287e7-ec70-47f6-a0be-610f6d79cc7e
    field: record
    value:
      concept: tc-9706ac56-d951-4eb6-9f27-cf7baa983a81
      language: en
      id: tm-75b287e7-ec70-47f6-a0be-610f6d79cc7e
      text: Pareto principle
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: juran-1974-non-pareto
        locator: https://www.juran.com/wp-content/uploads/2021/03/The-Non-Pareto-Principle-1974.pdf，PDF page index 0-2（印刷页
          1-3），lines 1-21、158-168、194-209
        checked: '2026-09-06'
  - identity: terms/terms/tm-13c4955e-8bec-4ddf-8a06-f8b061153bdf
    field: record
    value:
      concept: tc-9706ac56-d951-4eb6-9f27-cf7baa983a81
      language: zh-Hans
      id: tm-13c4955e-8bec-4ddf-8a06-f8b061153bdf
      text: 帕累托原则
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 帕累托原则是管理与质量领域对关键少数现象的行业表达，不把它改成项目选材义务；仅判断既有概念的行业表达，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-b3f9d941-2f49-425c-9e98-6b4e61b4444c
    field: record
    value:
      concept: tc-39065fa2-767d-4606-840c-aaffa5182661
      language: en
      id: tm-b3f9d941-2f49-425c-9e98-6b4e61b4444c
      text: monohierarchical structure
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.34；docs/references/iso-25964.md 已核定义表
        checked: '2026-08-29'
  - identity: terms/terms/tm-7b60cc0e-5b50-4047-b76b-91ff8a4cbdac
    field: record
    value:
      concept: tc-39065fa2-767d-4606-840c-aaffa5182661
      language: en
      id: tm-7b60cc0e-5b50-4047-b76b-91ff8a4cbdac
      text: monohierarchy
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: dunn-bourcier-nomenclature
        locator: §6 Limitations：monohierarchical classification system每词只有一个直接broader，随后monohierarchy回指
        checked: '2026-09-06'
  - identity: terms/terms/tm-9ae59983-3054-4e4b-9e59-e400bd6bffdf
    field: record
    value:
      concept: tc-39065fa2-767d-4606-840c-aaffa5182661
      language: zh-Hans
      id: tm-9ae59983-3054-4e4b-9e59-e400bd6bffdf
      text: 单层级
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 单层级在词表领域表示每个概念只有一个直接上位概念，而非只有一层深度；仅为既有概念的模型知识译名判断，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-57b80a57-9a91-4320-854d-e326cb9d52fa
    field: record
    value:
      concept: tc-025cc053-edb1-4def-a58f-1de00a8424a4
      language: en
      id: tm-57b80a57-9a91-4320-854d-e326cb9d52fa
      text: polyhierarchical structure
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.42；docs/references/iso-25964.md 已核定义表
        checked: '2026-08-29'
  - identity: terms/terms/tm-e2104559-047a-41be-84e5-dbe80f7d052f
    field: record
    value:
      concept: tc-025cc053-edb1-4def-a58f-1de00a8424a4
      language: en
      id: tm-e2104559-047a-41be-84e5-dbe80f7d052f
      text: polyhierarchy
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §5.4.3 taxonomy；§8.3.4 Polyhierarchical Relationships及Examples109–111
        checked: '2026-09-06'
  - identity: terms/terms/tm-e4c630f1-5986-4325-93a0-bc9710a3bab1
    field: record
    value:
      concept: tc-025cc053-edb1-4def-a58f-1de00a8424a4
      language: zh-Hans
      id: tm-e4c630f1-5986-4325-93a0-bc9710a3bab1
      text: 多层级
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 多层级在此表示概念允许多个上位概念，而非树的深度较大；仅为既有概念的模型知识译名判断，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-fd044b18-8d70-430b-b64e-2c81f72632cf
    field: record
    value:
      concept: tc-98d2d330-cabe-493f-8453-104822e92a0d
      language: en
      id: tm-fd044b18-8d70-430b-b64e-2c81f72632cf
      text: interoperability
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.29；docs/references/iso-25964.md 已核定义表
        checked: '2026-08-29'
  - identity: terms/terms/tm-4270711e-8a98-48d0-9ba3-5a1fc25eaf22
    field: record
    value:
      concept: tc-98d2d330-cabe-493f-8453-104822e92a0d
      language: zh-Hans
      id: tm-4270711e-8a98-48d0-9ba3-5a1fc25eaf22
      text: 互操作性
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 互操作性同时包括信息交换与使用，不能仅等同文件可导入；仅为既有概念的模型知识译名判断，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-77ec69a0-9cb0-48f7-8194-1adae82bdbf6
    field: record
    value:
      concept: tc-79c1fd4b-5f06-4d1e-a8d8-cd323c441939
      language: en
      id: tm-77ec69a0-9cb0-48f7-8194-1adae82bdbf6
      text: entity
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hogan-paper
        locator: P1 L72–L88；nodes represent entities 与 identity 讨论；work/reviews/2026-09-06-term-web-model-coverage.json
        checked: '2026-09-06'
  - identity: terms/terms/tm-9fb55b4b-7fe8-475f-a552-10bd90c5855d
    field: record
    value:
      concept: tc-79c1fd4b-5f06-4d1e-a8d8-cd323c441939
      language: zh-Hans
      id: tm-9fb55b4b-7fe8-475f-a552-10bd90c5855d
      text: 实体
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 实体是知识表示领域对被表示对象的行业称呼，不把实体等同于图节点或标识符。外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-a91f7e4f-a2bb-4681-ba36-86d3529b7cbe
    field: record
    value:
      concept: tc-605b0308-57af-486b-81ba-81e18b993b07
      language: en
      id: tm-a91f7e4f-a2bb-4681-ba36-86d3529b7cbe
      text: property
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hogan-paper
        locator: P6 L316–L322；property graph 中 nodes/edges 关联 property–value pairs；work/reviews/2026-09-06-term-web-model-coverage.json
        checked: '2026-09-06'
  - identity: terms/terms/tm-16fe2abb-fe52-4f08-97a4-5bb36f6c2f15
    field: record
    value:
      concept: tc-605b0308-57af-486b-81ba-81e18b993b07
      language: zh-Hans
      id: tm-16fe2abb-fe52-4f08-97a4-5bb36f6c2f15
      text: 属性
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 属性是图数据模型中描述节点或边特征的信息；本条明确属性图语境，并区别属性名与其值。外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-29e4f758-6d4f-4411-b474-e1f08b3213ae
    field: record
    value:
      concept: tc-4f002e0f-1fe2-41e5-a15c-3cdb436b1763
      language: en
      id: tm-29e4f758-6d4f-4411-b474-e1f08b3213ae
      text: classification scheme
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.6，免费样章印刷p.2
        checked: '2026-09-06'
  - identity: terms/terms/tm-4011c8e8-cd44-497e-85f0-1667007d53c7
    field: record
    value:
      concept: tc-4f002e0f-1fe2-41e5-a15c-3cdb436b1763
      language: zh-Hans
      id: tm-4011c8e8-cd44-497e-85f0-1667007d53c7
      text: 分类表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 分类表指按分类组织的概念表，不替换成taxonomy或一般分类操作。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-6d783441-c3df-409b-8202-742ff6b3bfa4
    field: record
    value:
      concept: tc-84906e82-1b72-4118-951c-33416d9d9bf7
      language: en
      id: tm-6d783441-c3df-409b-8202-742ff6b3bfa4
      text: term
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §4.1 Glossary，term
        checked: '2026-09-06'
  - identity: terms/terms/tm-868a4b9a-45b4-4d9f-b359-8de7a44f060f
    field: record
    value:
      concept: tc-84906e82-1b72-4118-951c-33416d9d9bf7
      language: zh-Hans
      id: tm-868a4b9a-45b4-4d9f-b359-8de7a44f060f
      text: 词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: NISO已核term意义与原概念一致；英文名称保留，中文词在本条也包含多词表达，不冒称ISO§2.61已读。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-ba65904c-7386-439b-9b62-d2fbb3024a94
    field: record
    value:
      concept: tc-c5ee911a-276c-4bc1-81e7-f651972b0830
      language: en
      id: tm-ba65904c-7386-439b-9b62-d2fbb3024a94
      text: entry term
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.16，免费样章印刷p.4
        checked: '2026-09-06'
  - identity: terms/terms/tm-87280583-a819-4fba-a27d-83bfb9035805
    field: record
    value:
      concept: tc-c5ee911a-276c-4bc1-81e7-f651972b0830
      language: en
      id: tm-87280583-a819-4fba-a27d-83bfb9035805
      text: lead-in term
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.16，免费样章印刷p.4
        checked: '2026-09-06'
  - identity: terms/terms/tm-c15bae24-b66d-4da9-bb5b-cd84d38fd50c
    field: record
    value:
      concept: tc-c5ee911a-276c-4bc1-81e7-f651972b0830
      language: zh-Hans
      id: tm-c15bae24-b66d-4da9-bb5b-cd84d38fd50c
      text: 入口词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 入口词强调通向可用术语的检索入口，不等于所有标引词。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-9c6430b5-c331-4cf0-943a-5cae137ca58d
    field: record
    value:
      concept: tc-57a8d816-05c4-4aa9-b3da-277b5d23cc4e
      language: en
      id: tm-9c6430b5-c331-4cf0-943a-5cae137ca58d
      text: hidden label
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: skos
        locator: §5 Lexical Labels；skos:hiddenLabel及示例
        checked: '2026-09-06'
  - identity: terms/terms/tm-3c495c32-6257-4fc1-8ecf-e60a823d33da
    field: record
    value:
      concept: tc-57a8d816-05c4-4aa9-b3da-277b5d23cc4e
      language: zh-Hans
      id: tm-3c495c32-6257-4fc1-8ecf-e60a823d33da
      text: 隐藏标签
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 隐藏标签对应可检索但不直接显示的词汇标签；ISO hidden布尔输出标志只作模型背景，不声称两个接口完全等价。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-c9a7fa2f-a37c-4f88-83bd-aed4e2b88613
    field: record
    value:
      concept: tc-d58d9afb-92ca-46c1-b928-e6ea6c2a11a6
      language: en
      id: tm-c9a7fa2f-a37c-4f88-83bd-aed4e2b88613
      text: homograph
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.24，免费样章印刷p.6
        checked: '2026-09-06'
  - identity: terms/terms/tm-d4d7539d-7a93-487d-ba5b-d94d3b3fdbf0
    field: record
    value:
      concept: tc-d58d9afb-92ca-46c1-b928-e6ea6c2a11a6
      language: zh-Hans
      id: tm-d4d7539d-7a93-487d-ba5b-d94d3b3fdbf0
      text: 同形异义词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 同形异义词同时保留相同字形与不同意义这两个判据。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-3cd0a683-a19a-4073-8f06-87e6540ec09c
    field: record
    value:
      concept: tc-adbb6019-db11-4d1e-a9b2-4e7a8fedd0a5
      language: en
      id: tm-3cd0a683-a19a-4073-8f06-87e6540ec09c
      text: quasi-synonym
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.47，免费样章印刷p.9
        checked: '2026-09-06'
  - identity: terms/terms/tm-b56a70b0-92c7-460b-a1ca-9d5d5cf27dcb
    field: record
    value:
      concept: tc-adbb6019-db11-4d1e-a9b2-4e7a8fedd0a5
      language: zh-Hans
      id: tm-b56a70b0-92c7-460b-a1ca-9d5d5cf27dcb
      text: 准同义词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 准同义词是特定词表中的约定等价，非日常语言完全同义。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-427e5a68-a3c5-4be6-9337-f84962686067
    field: record
    value:
      concept: tc-a977c939-c9fe-477b-a154-a0ccd97aa3d6
      language: en
      id: tm-427e5a68-a3c5-4be6-9337-f84962686067
      text: compound term
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.9，免费样章印刷p.3
        checked: '2026-09-06'
  - identity: terms/terms/tm-2d65f52c-42b6-464f-9208-f4cb567df8db
    field: record
    value:
      concept: tc-a977c939-c9fe-477b-a154-a0ccd97aa3d6
      language: zh-Hans
      id: tm-2d65f52c-42b6-464f-9208-f4cb567df8db
      text: 复合词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 复合词按形态可拆分确定，不仅是有空格的多词短语。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-bb629eab-c872-4e13-a921-7c7577afb769
    field: record
    value:
      concept: tc-b0214996-65e1-4d37-a055-b7356a776ac0
      language: en
      id: tm-bb629eab-c872-4e13-a921-7c7577afb769
      text: complex concept
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: will-2012-iso-data-model
        locator: Compound Equivalence，L94–101，coal mining同例compound concept与complex concept回指
        checked: '2026-09-06'
  - identity: terms/terms/tm-f33000a3-3b8c-467d-9731-9a83c28bfe76
    field: record
    value:
      concept: tc-b0214996-65e1-4d37-a055-b7356a776ac0
      language: zh-Hans
      id: tm-f33000a3-3b8c-467d-9731-9a83c28bfe76
      text: 复合概念
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 复合概念的旧英文complex concept在作者同段直接出现，意义与原组合概念一致，不自动新增coal mining等示例概念。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-d1b26431-6581-44bf-929d-095b69ca660f
    field: record
    value:
      concept: tc-6a20995f-a6b2-492a-88e9-a554c8364fe2
      language: en
      id: tm-d1b26431-6581-44bf-929d-095b69ca660f
      text: domain
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-1087-2019
        locator: §3.1.4，PDFp.7/印刷p.1，注释续p.8
        checked: '2026-09-06'
  - identity: terms/terms/tm-8fc9be24-693d-4905-a110-353c793cf283
    field: record
    value:
      concept: tc-6a20995f-a6b2-492a-88e9-a554c8364fe2
      language: zh-Hans
      id: tm-8fc9be24-693d-4905-a110-353c793cf283
      text: 领域
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 领域是专门知识范围的行业名称；本库用于说明词表覆盖范围，应用用法另说明，不等于网络域。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-067d0bdf-9db2-490f-a6a8-301b3ec0ee1f
    field: record
    value:
      concept: tc-a8e5c450-33ff-42e5-a352-1bbb21fcd0b5
      language: en
      id: tm-067d0bdf-9db2-490f-a6a8-301b3ec0ee1f
      text: metadata
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.33，免费样章印刷p.6
        checked: '2026-09-06'
  - identity: terms/terms/tm-92599d5f-6dad-4f51-a4b9-379f8e14ac85
    field: record
    value:
      concept: tc-a8e5c450-33ff-42e5-a352-1bbb21fcd0b5
      language: zh-Hans
      id: tm-92599d5f-6dad-4f51-a4b9-379f8e14ac85
      text: 元数据
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 元数据保留文档属性描述的原语境；首选词可作元数据值是来源补充说明。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-2295a8c2-8677-4bf0-97fc-b962cad6bc4a
    field: record
    value:
      concept: tc-ad90ba40-f5b0-44e7-9f59-fa2783d837b3
      language: zh-Hans
      id: tm-2295a8c2-8677-4bf0-97fc-b962cad6bc4a
      text: 复合等价
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 复合等价指一对多的概念或名称表示；USE+/UF+是符号，不造英文术语。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-0e54e5ec-61e2-412f-8e2a-1ac13804a53f
    field: record
    value:
      concept: tc-54e74c2d-103e-4935-aab7-fb44a129af69
      language: zh-Hans
      id: tm-0e54e5ec-61e2-412f-8e2a-1ac13804a53f
      text: 属种关系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 属种关系是类与子类的全部/部分关系，不把个别实例属于类混入；原BTG/NTG只作关系指示符。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-4a9bb6d7-1099-41e8-be65-a9da97d0073a
    field: record
    value:
      concept: tc-818463b8-0d48-4ddf-98fb-228ef4591308
      language: zh-Hans
      id: tm-4a9bb6d7-1099-41e8-be65-a9da97d0073a
      text: 整部关系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 整部关系保留整体/部分机制，不能把任意关联解释为部分；原BTP/NTP为符号。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-64b1efd6-53a5-4b7e-827c-0edfdadd6ba2
    field: record
    value:
      concept: tc-9fde9fd8-eb29-4477-acc1-295f9de9adf5
      language: zh-Hans
      id: tm-64b1efd6-53a5-4b7e-827c-0edfdadd6ba2
      text: 实例关系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 实例关系的两端是类与个体，不是类与子类；原BTI/NTI为符号。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-dd400c8e-6f1f-4f2b-a787-1b9290e16e7d
    field: record
    value:
      concept: tc-a529619b-cbcb-4545-901d-54f72971e76f
      language: zh-Hans
      id: tm-dd400c8e-6f1f-4f2b-a787-1b9290e16e7d
      text: 自定义关系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 自定义关系表达类型细分机制，依据为配套工件而非未读ISO§10.4；不授权本库实际新增任何关系类型。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-572d4ac7-3aae-4823-83e3-fddeedba662e
    field: record
    value:
      concept: tc-df2d8160-1717-4372-a38f-db96925ac980
      language: en
      id: tm-572d4ac7-3aae-4823-83e3-fddeedba662e
      text: paradigmatic relationship
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.41 paradigmatic relationship / a priori relationship，印刷p.8
        checked: '2026-09-06'
  - identity: terms/terms/tm-d5659ae3-56dd-4e82-ac4e-cc45fcce05a5
    field: record
    value:
      concept: tc-df2d8160-1717-4372-a38f-db96925ac980
      language: zh-Hans
      id: tm-d5659ae3-56dd-4e82-ac4e-cc45fcce05a5
      text: 聚合关系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 聚合关系保留概念内在语义，区别随文档语境形成的组合关系。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-ccdfadf2-0216-4f91-aa21-d7a4d1f5b8bd
    field: record
    value:
      concept: tc-1b0b91bc-d29e-44d4-854c-cddd05aebc13
      language: en
      id: tm-ccdfadf2-0216-4f91-aa21-d7a4d1f5b8bd
      text: syntagmatic relationship
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: mazzocchi-knowledge-organization-system
        locator: §5.1 a priori/a posteriori与paradigmatic/syntagmatic段
        checked: '2026-09-06'
  - identity: terms/terms/tm-3dc5c513-2684-4789-b88b-2a74897fb869
    field: record
    value:
      concept: tc-1b0b91bc-d29e-44d4-854c-cddd05aebc13
      language: zh-Hans
      id: tm-3dc5c513-2684-4789-b88b-2a74897fb869
      text: 组合关系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 组合关系依语境建立，不等于同篇出现就必有语义关系；不把作者说明写成已读ISO§4.3。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-34ed6873-0990-469c-b505-518e69018077
    field: record
    value:
      concept: tc-b10cded9-f3ab-4cdd-b218-edb279779c33
      language: en
      id: tm-34ed6873-0990-469c-b505-518e69018077
      text: reciprocal
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §4.1 reciprocal；§5.4.4 relationship indicators reciprocally；§8.3
        checked: '2026-09-06'
  - identity: terms/terms/tm-2509c694-0529-422a-8c8c-16b9cc377310
    field: record
    value:
      concept: tc-b10cded9-f3ab-4cdd-b218-edb279779c33
      language: zh-Hans
      id: tm-2509c694-0529-422a-8c8c-16b9cc377310
      text: 互反
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 互反表示反向关系配对；不把关系概念直接变成本库必须物理双写的实现规则。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-bbbe8ecb-22ce-4f7d-a526-5b051b058056
    field: record
    value:
      concept: tc-af0edf3d-0500-4fc7-bad0-39127321295c
      language: en
      id: tm-bbbe8ecb-22ce-4f7d-a526-5b051b058056
      text: hierarchy
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §8.3与§8.3.4，印刷pp.47–50
        checked: '2026-09-06'
  - identity: terms/terms/tm-a8384214-a207-4a7c-9fd0-4313fdb5b353
    field: record
    value:
      concept: tc-af0edf3d-0500-4fc7-bad0-39127321295c
      language: zh-Hans
      id: tm-a8384214-a207-4a7c-9fd0-4313fdb5b353
      text: 层级
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 层级是上下位安排，允许多上位；不能与严格树结构无条件同义。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-3b55a969-53ac-4622-ab97-d7774a558335
    field: record
    value:
      concept: tc-7d9ce2a6-2d92-49c3-8d22-c771cdaae4c3
      language: en
      id: tm-3b55a969-53ac-4622-ab97-d7774a558335
      text: tree
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: nist-dads-tree
        locator: Definition(1)及Formal Definition，2017-12-15
        checked: '2026-09-06'
  - identity: terms/terms/tm-083afbe6-20c8-47c6-9d23-a51bdd0c2549
    field: record
    value:
      concept: tc-7d9ce2a6-2d92-49c3-8d22-c771cdaae4c3
      language: zh-Hans
      id: tm-083afbe6-20c8-47c6-9d23-a51bdd0c2549
      text: 树
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 树保留原中文独立结构概念，按NIST定义区别于可有多上位的一般层级；英文tree为源有依据的补充形式。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-17074702-584d-4331-acfa-2c2e88627670
    field: record
    value:
      concept: tc-2cc8c45b-bf02-4b54-bbfc-86286dbd50d7
      language: en
      id: tm-17074702-584d-4331-acfa-2c2e88627670
      text: node
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: nist-dads-node
        locator: Definition(1)，2004-12-17
        checked: '2026-09-06'
  - identity: terms/terms/tm-abffcb75-f9c9-43fa-bf71-798a140d5b48
    field: record
    value:
      concept: tc-2cc8c45b-bf02-4b54-bbfc-86286dbd50d7
      language: zh-Hans
      id: tm-abffcb75-f9c9-43fa-bf71-798a140d5b48
      text: 节点
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 节点在本行限于图/树结构；本库以节点表示概念是应用说明，不进入NIST定义。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-2c29e44a-28e1-430a-bc45-252c6f067a30
    field: record
    value:
      concept: tc-6d0b88b7-c403-48bf-9579-b2d94dbf9502
      language: en
      id: tm-2c29e44a-28e1-430a-bc45-252c6f067a30
      text: top concept
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso25964-xsd-1-4
        locator: ThesaurusConceptStruct/topConcept documentation
        checked: '2026-09-06'
  - identity: terms/terms/tm-30908171-1a13-4cb7-b754-48b0014eea6f
    field: record
    value:
      concept: tc-6d0b88b7-c403-48bf-9579-b2d94dbf9502
      language: zh-Hans
      id: tm-30908171-1a13-4cb7-b754-48b0014eea6f
      text: 顶层概念
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 顶层概念按没有broader确定，不是显示窗口中暂时最上的节点。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-4b576cd0-ac19-4ef6-883b-72e82977549c
    field: record
    value:
      concept: tc-6bd16590-fd5e-4cee-9c8b-881051af3706
      language: en
      id: tm-4b576cd0-ac19-4ef6-883b-72e82977549c
      text: microthesaurus
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.46，PDFindex13/印刷p.8
        checked: '2026-09-06'
  - identity: terms/terms/tm-c6e74d84-b72d-47ae-9b25-bc9896c878ca
    field: record
    value:
      concept: tc-6bd16590-fd5e-4cee-9c8b-881051af3706
      language: en
      id: tm-c6e74d84-b72d-47ae-9b25-bc9896c878ca
      text: micro-thesaurus
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.46，PDFindex13/印刷p.8
        checked: '2026-09-06'
  - identity: terms/terms/tm-39d989b6-114d-4482-823a-e6d505597c0c
    field: record
    value:
      concept: tc-6bd16590-fd5e-4cee-9c8b-881051af3706
      language: zh-Hans
      id: tm-39d989b6-114d-4482-823a-e6d505597c0c
      text: 微词表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 微词表强调子集可独立作为完整叙词表运行；是否实际建立子库不由词条采纳决定。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-3fd9be57-3134-4fdb-83ac-4e4288f39ab5
    field: record
    value:
      concept: tc-81fc1070-a33d-4692-b613-751819cecc3b
      language: en
      id: tm-3fd9be57-3134-4fdb-83ac-4e4288f39ab5
      text: auxiliary table
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: w3c-udc-use-case
        locator: L22 special auxiliaries；L56–57 common auxiliaries及tables，L68–80组合案例
        checked: '2026-09-06'
  - identity: terms/terms/tm-1db6403d-e157-42c0-9d03-d9c6bafaef9e
    field: record
    value:
      concept: tc-81fc1070-a33d-4692-b613-751819cecc3b
      language: zh-Hans
      id: tm-1db6403d-e157-42c0-9d03-d9c6bafaef9e
      text: 辅助表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 辅助表说明复用分类特征机制；原只通用维度、只尾部拼接过窄，固定作者案例同时展示专用与通用。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-b4a8055d-5598-4ea1-bc76-e35428986632
    field: record
    value:
      concept: tc-81fc1070-a33d-4692-b613-751819cecc3b
      language: zh-Hans
      id: tm-b4a8055d-5598-4ea1-bc76-e35428986632
      text: 复分表
      administrative_status: admittedTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 复分表是分类实践中以可重复特征进一步细分类号的既有中文称呼；本条与辅助表同限配合主表使用的分类表，不泛指任意再次划分。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-c465bee5-b846-4fc6-879b-26642d41fca3
    field: record
    value:
      concept: tc-2f3dc564-3adc-46d7-ba3c-4051eaaa434c
      language: en
      id: tm-c465bee5-b846-4fc6-879b-26642d41fca3
      text: synthesized notation
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: w3c-udc-use-case
        locator: L56–80组合通用辅助号/主号与复合主题；参ISO25964-1§2.22上下文
        checked: '2026-09-06'
  - identity: terms/terms/tm-23343b8e-95df-4574-a499-8cdf75d77e8c
    field: record
    value:
      concept: tc-2f3dc564-3adc-46d7-ba3c-4051eaaa434c
      language: zh-Hans
      id: tm-23343b8e-95df-4574-a499-8cdf75d77e8c
      text: 组配号
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 组配号是组合所得分类记号，区别标示分面开始的facet indicator；原ISO条目错位明确纠正。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-3b1cb85c-480e-4e19-a3ef-5b868cd6a3cb
    field: record
    value:
      concept: tc-a4f76dad-bbea-4cf0-b322-1c689c380d95
      language: en
      id: tm-3b1cb85c-480e-4e19-a3ef-5b868cd6a3cb
      text: pre-coordination
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.44，免费样章印刷p.9
        checked: '2026-09-06'
  - identity: terms/terms/tm-72449164-9665-4eed-bd23-9198392d3432
    field: record
    value:
      concept: tc-a4f76dad-bbea-4cf0-b322-1c689c380d95
      language: zh-Hans
      id: tm-72449164-9665-4eed-bd23-9198392d3432
      text: 先组
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 先组按组合发生在构建/标引阶段界定，不把多词形式自动等同先组。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-3b58953d-02b2-4956-947e-b60779dfca0d
    field: record
    value:
      concept: tc-7fd3d9b0-be29-4f3c-a5a6-7817f26d9391
      language: en
      id: tm-3b58953d-02b2-4956-947e-b60779dfca0d
      text: post-coordination
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-1
        locator: §2.43，免费样章印刷p.9
        checked: '2026-09-06'
  - identity: terms/terms/tm-dd7d2f60-4b07-447c-bc5f-f06d5724fa19
    field: record
    value:
      concept: tc-7fd3d9b0-be29-4f3c-a5a6-7817f26d9391
      language: zh-Hans
      id: tm-dd7d2f60-4b07-447c-bc5f-f06d5724fa19
      text: 后组
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 后组的区别在检索时组合，与先组作时点对照。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-16a66968-e1b1-4709-9f46-a3dd2964c067
    field: record
    value:
      concept: tc-7cee3db8-8807-48b2-9fe8-7f0fe0539272
      language: en
      id: tm-16a66968-e1b1-4709-9f46-a3dd2964c067
      text: attribute
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hearst-2009-search-user-interfaces
        locator: §8.3 attribute/dimension同例；§8.6 facet/dimension/feature type
        checked: '2026-09-06'
  - identity: terms/terms/tm-a7e2d2bf-bd4f-42c6-a0dd-39cc88a90373
    field: record
    value:
      concept: tc-7cee3db8-8807-48b2-9fe8-7f0fe0539272
      language: en
      id: tm-a7e2d2bf-bd4f-42c6-a0dd-39cc88a90373
      text: dimension
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: hearst-2009-search-user-interfaces
        locator: §8.3 attribute/dimension同例；§8.6 facet/dimension/feature type
        checked: '2026-09-06'
  - identity: terms/terms/tm-67e8828c-7806-42b2-a9f1-b0053cf14a54
    field: record
    value:
      concept: tc-7cee3db8-8807-48b2-9fe8-7f0fe0539272
      language: zh-Hans
      id: tm-67e8828c-7806-42b2-a9f1-b0053cf14a54
      text: 属性
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 属性是内容对象的特性，不是存储字段本身；与知识图谱property另一个概念分开。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-2c3da61d-f341-4d0d-9614-aefc3c6f7a3f
    field: record
    value:
      concept: tc-7cee3db8-8807-48b2-9fe8-7f0fe0539272
      language: zh-Hans
      id: tm-2c3da61d-f341-4d0d-9614-aefc3c6f7a3f
      text: 维度
      administrative_status: admittedTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 维度在本条仅指描述或检索内容对象的特性方面，与attribute同一受限范围；不等同所有数学维度或分面结构。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-4b5fc7e6-51b3-47af-8068-ea2df1fca97a
    field: record
    value:
      concept: tc-549f2d8d-7ddd-4bd3-b6e1-74e815f9feb2
      language: en
      id: tm-4b5fc7e6-51b3-47af-8068-ea2df1fca97a
      text: definition
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-1087-2019
        locator: §3.3.1，PDFp.12/印刷p.6
        checked: '2026-09-06'
  - identity: terms/terms/tm-7ecbf405-7181-4a27-ae54-3cc83dafd16e
    field: record
    value:
      concept: tc-549f2d8d-7ddd-4bd3-b6e1-74e815f9feb2
      language: zh-Hans
      id: tm-7ecbf405-7181-4a27-ae54-3cc83dafd16e
      text: 定义
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 定义的意义由ISO1087支持；ISO25964的Definition类只是存放位置说明，不替代一般概念。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-7595b7a0-4cc9-4006-8158-8e6e21dc605d
    field: record
    value:
      concept: tc-d6a34d9f-e8f9-4170-9d62-e5b3676e71d9
      language: en
      id: tm-7595b7a0-4cc9-4006-8158-8e6e21dc605d
      text: editorial note
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso25964-xsd-1-4
        locator: EditorialNote documentation
        checked: '2026-09-06'
  - identity: terms/terms/tm-50a8107f-fb70-4df7-be97-59c8f5ac72e8
    field: record
    value:
      concept: tc-d6a34d9f-e8f9-4170-9d62-e5b3676e71d9
      language: zh-Hans
      id: tm-50a8107f-fb70-4df7-be97-59c8f5ac72e8
      text: 编辑注释
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 编辑注释服务编辑过程，区别供用户理解概念范围的注释。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-5ec44c1d-1d30-4952-8a28-d82bc54f7669
    field: record
    value:
      concept: tc-82db3b46-353e-405f-8a8d-fd6fee70bdb5
      language: en
      id: tm-5ec44c1d-1d30-4952-8a28-d82bc54f7669
      text: deprecated term
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-1087-2019
        locator: §3.4.21，GSO公开HTML预览；对照§3.4.22 obsolete term
        checked: '2026-09-06'
  - identity: terms/terms/tm-e1b7439c-738a-4056-9c53-8e96b4b7d5ef
    field: record
    value:
      concept: tc-82db3b46-353e-405f-8a8d-fd6fee70bdb5
      language: zh-Hans
      id: tm-e1b7439c-738a-4056-9c53-8e96b4b7d5ef
      text: 废弃词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 废弃词指不宜使用的名称评价，不自动包含删除、保留或替代链的项目操作；与不再常用的obsolete区别。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-da14faa1-b603-4b39-9e6c-37a797c42b2b
    field: record
    value:
      concept: tc-504af76c-f69e-469e-8e73-239f2fd3da99
      language: en
      id: tm-da14faa1-b603-4b39-9e6c-37a797c42b2b
      text: status
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso25964-xsd-1-4
        locator: ThesaurusConceptStruct/status与ThesaurusTerm/status文档注记
        checked: '2026-09-06'
  - identity: terms/terms/tm-f9159807-4154-4be9-8a5c-4039896902fa
    field: record
    value:
      concept: tc-504af76c-f69e-469e-8e73-239f2fd3da99
      language: zh-Hans
      id: tm-f9159807-4154-4be9-8a5c-4039896902fa
      text: 状态
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 状态是阶段属性，来源示例值不覆盖本库状态机。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-ec43572b-e2e5-4c4a-8fb1-6be8931c3635
    field: record
    value:
      concept: tc-f4802cd3-fba8-4bb1-89a0-121eebbf1fc6
      language: en
      id: tm-ec43572b-e2e5-4c4a-8fb1-6be8931c3635
      text: version history
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: will-2012-iso-data-model
        locator: Version History，L145–147，自然英文version history直接出现
        checked: '2026-09-06'
  - identity: terms/terms/tm-9ac2e455-f438-460f-ad02-baf7377a105d
    field: record
    value:
      concept: tc-f4802cd3-fba8-4bb1-89a0-121eebbf1fc6
      language: zh-Hans
      id: tm-9ac2e455-f438-460f-ad02-baf7377a105d
      text: 版本历史
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 版本历史记录词表整体版次，非单条术语的变更历史；不再依靠CamelCase拆词推断形式。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-1bf1d191-63fe-4c9e-9761-a2543c13f382
    field: record
    value:
      concept: tc-d529a566-45fc-44f0-8b92-0eca58807137
      language: en
      id: tm-1bf1d191-63fe-4c9e-9761-a2543c13f382
      text: warrant
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §5.3.5 Warrant，印刷p.16
        checked: '2026-09-06'
  - identity: terms/terms/tm-f188b119-c518-45fa-986c-67d6f6801238
    field: record
    value:
      concept: tc-d529a566-45fc-44f0-8b92-0eca58807137
      language: zh-Hans
      id: tm-f188b119-c518-45fa-986c-67d6f6801238
      text: 依据
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 依据在此限定收词选择，不泛化成任意字段basis。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-9c96c16a-7bfc-4949-8ebb-1d44e3ae2d49
    field: record
    value:
      concept: tc-8b56b1d2-7fd1-499b-8085-a9dd926e4c28
      language: en
      id: tm-9c96c16a-7bfc-4949-8ebb-1d44e3ae2d49
      text: analytico-synthetic classification
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hjorland-facet-analysis
        locator: §3 Basic principles of facet analysis
        checked: '2026-09-06'
  - identity: terms/terms/tm-5a5ad88a-778f-4cb4-ae7f-3e586fc400a2
    field: record
    value:
      concept: tc-8b56b1d2-7fd1-499b-8085-a9dd926e4c28
      language: zh-Hans
      id: tm-5a5ad88a-778f-4cb4-ae7f-3e586fc400a2
      text: 分析综合式分类
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 分析综合式分类保留先分析后综合机制；作者后续原文可作定义依据，不伪报已读Ranganathan1957。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-80141b21-b90d-4ca3-8735-7a022c1a88b1
    field: record
    value:
      concept: tc-b888a0b9-0011-4e55-b6a5-bb01e56b79aa
      language: en
      id: tm-80141b21-b90d-4ca3-8735-7a022c1a88b1
      text: canon of hospitality
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: kaula-1980-canons
        locator: §2，印刷p.118；§7/7.1/7.2，印刷p.125
        checked: '2026-09-06'
  - identity: terms/terms/tm-4fa46a60-3253-406e-b720-84673ef1bdc4
    field: record
    value:
      concept: tc-b888a0b9-0011-4e55-b6a5-bb01e56b79aa
      language: zh-Hans
      id: tm-4fa46a60-3253-406e-b720-84673ef1bdc4
      text: 好客准则
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 好客准则在分类学中指容纳新类目的能力，保留数组和链两个方面，不新增两种概念。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-5efaa936-a3bb-4f9a-b5c9-e2a3d64af7de
    field: record
    value:
      concept: tc-f91d813f-7dfd-4aae-9198-756996799dd3
      language: en
      id: tm-5efaa936-a3bb-4f9a-b5c9-e2a3d64af7de
      text: domain analysis
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hjorland-domain-analysis
        locator: §1.1/1.2/1.4/2.1/4.7/7；作者实际网页正文
        checked: '2026-09-06'
  - identity: terms/terms/tm-aa71dcf0-b589-4daf-8125-e27672bebe75
    field: record
    value:
      concept: tc-f91d813f-7dfd-4aae-9198-756996799dd3
      language: zh-Hans
      id: tm-aa71dcf0-b589-4daf-8125-e27672bebe75
      text: 领域分析
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 领域分析保留LIS中的共同体、专门知识与认识论机制；不换成软件工程domain analysis，不将没有唯一正确分类写成绝对定律。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-135147b0-7149-4c14-9d10-d4863a83edf2
    field: record
    value:
      concept: tc-b96d261a-9203-4f68-8b78-92e2667818ea
      language: en
      id: tm-135147b0-7149-4c14-9d10-d4863a83edf2
      text: residual category
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: star-bowker-2007-enacting-silence
        locator: 原作者论文Abstract，Ethics and Information Technology9(2007)273–280
        checked: '2026-09-06'
  - identity: terms/terms/tm-ef7fbfce-26f3-4f02-aa2d-ec9380f73b15
    field: record
    value:
      concept: tc-b96d261a-9203-4f68-8b78-92e2667818ea
      language: zh-Hans
      id: tm-ef7fbfce-26f3-4f02-aa2d-ec9380f73b15
      text: 剩余类目
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 剩余类目以分类无法正式表示为边界；旧其他/杂项是例子，大小必然说明失效的断言没有随定义采纳。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-f8d9b426-d08f-4ea6-a77d-ca28e4261912
    field: record
    value:
      concept: tc-d123d909-3897-427f-9e04-e31d9072176c
      language: en
      id: tm-f8d9b426-d08f-4ea6-a77d-ca28e4261912
      text: indexing
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.36，PDFp.12，原始读取L470–486
        checked: '2026-09-06'
  - identity: terms/terms/tm-8d8dd91c-4bfe-42e2-84b3-f30e00b13677
    field: record
    value:
      concept: tc-d123d909-3897-427f-9e04-e31d9072176c
      language: zh-Hans
      id: tm-8d8dd91c-4bfe-42e2-84b3-f30e00b13677
      text: 标引
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 标引既有主题分析又有分配术语；引用实际已读Part2定义，不把原Part1定位伪称重读。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-0a9be29e-5fb3-4d41-b287-80801423734c
    field: record
    value:
      concept: tc-7e07c6f9-8677-4b87-8e32-e23d72dbfe64
      language: en
      id: tm-0a9be29e-5fb3-4d41-b287-80801423734c
      text: index term
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.35，PDFp.12，L470–473
        checked: '2026-09-06'
  - identity: terms/terms/tm-f997b0b2-4bfa-4973-90c8-dc07241e3d22
    field: record
    value:
      concept: tc-7e07c6f9-8677-4b87-8e32-e23d72dbfe64
      language: zh-Hans
      id: tm-f997b0b2-4bfa-4973-90c8-dc07241e3d22
      text: 标引词
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 标引词由分配行为和文档对象界定；keyword/tag宽泛比较单列而不当必要定义。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-0b3df564-f31a-41b9-bcd8-ae62a8b5b2aa
    field: record
    value:
      concept: tc-c96ff99a-aef7-4d8d-b4d5-2c3e2835a64b
      language: en
      id: tm-0b3df564-f31a-41b9-bcd8-ae62a8b5b2aa
      text: mapping cluster
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.42，PDFp.12，L512–518
        checked: '2026-09-06'
  - identity: terms/terms/tm-3911501b-963b-4f98-abdb-d9f4cc97b7e5
    field: record
    value:
      concept: tc-c96ff99a-aef7-4d8d-b4d5-2c3e2835a64b
      language: zh-Hans
      id: tm-3911501b-963b-4f98-abdb-d9f4cc97b7e5
      text: 映射簇
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 映射簇是协调的多词表映射集合，保留原三个或更多的源定义条件。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-145bf65b-7bb4-4d85-9511-95c04d9dd084
    field: record
    value:
      concept: tc-dc56c863-cea8-485d-afcd-c606ce2a8a4b
      language: en
      id: tm-145bf65b-7bb4-4d85-9511-95c04d9dd084
      text: crosswalk
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.21，PDFp.9，L360–363
        checked: '2026-09-06'
  - identity: terms/terms/tm-5976ab3d-1bf1-424f-af90-3fc111527a8e
    field: record
    value:
      concept: tc-dc56c863-cea8-485d-afcd-c606ce2a8a4b
      language: zh-Hans
      id: tm-5976ab3d-1bf1-424f-af90-3fc111527a8e
      text: 对照表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 对照表严格指原词表层crosswalk；不复用已撤的metadata-crosswalk提案ID或更换概念。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-2549ff94-fbe5-4854-bbba-79a658e6e46a
    field: record
    value:
      concept: tc-14b64c1a-938e-4d43-8e05-e18e0dd4e4f3
      language: en
      id: tm-2549ff94-fbe5-4854-bbba-79a658e6e46a
      text: source vocabulary
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.27，PDFp.10，L401–405 source/target两端语境
        checked: '2026-09-06'
  - identity: terms/terms/tm-101132c3-86ad-4115-8d07-44caba815192
    field: record
    value:
      concept: tc-14b64c1a-938e-4d43-8e05-e18e0dd4e4f3
      language: zh-Hans
      id: tm-101132c3-86ad-4115-8d07-44caba815192
      text: 源词表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 源词表是映射中的一端角色；原并列两项分开，不当同义词，不需制造未读独立条款。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-7f2a566a-083a-48ee-9396-6cd2b7f100ff
    field: record
    value:
      concept: tc-b98ed928-3bbd-42a8-8f7f-b447c735b4c7
      language: en
      id: tm-7f2a566a-083a-48ee-9396-6cd2b7f100ff
      text: target vocabulary
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-25964-2
        locator: §3.27，PDFp.10，L401–405 source/target两端语境
        checked: '2026-09-06'
  - identity: terms/terms/tm-a946b241-c351-47b7-b4d8-e67a02a83c2c
    field: record
    value:
      concept: tc-b98ed928-3bbd-42a8-8f7f-b447c735b4c7
      language: zh-Hans
      id: tm-a946b241-c351-47b7-b4d8-e67a02a83c2c
      text: 目标词表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 目标词表是映射中的一端角色；原并列两项分开，不当同义词，不需制造未读独立条款。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-730b11b7-c904-4533-bdd1-ecaea57a3bf3
    field: record
    value:
      concept: tc-5d5225be-ab9d-44e4-866b-e321c998d766
      language: en
      id: tm-730b11b7-c904-4533-bdd1-ecaea57a3bf3
      text: exact equivalence
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: will-2009-skos-iso
        locator: Mapping between thesauri a–c；L131–140
        checked: '2026-09-06'
  - identity: terms/terms/tm-a10f14d1-2756-456f-90b1-754ad286e2a0
    field: record
    value:
      concept: tc-5d5225be-ab9d-44e4-866b-e321c998d766
      language: zh-Hans
      id: tm-a10f14d1-2756-456f-90b1-754ad286e2a0
      text: 精确等价
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 精确等价按Will2009明确范围判据解释；这是个人作者解释，不伪称ISO2013§11逐项核实或SKOS属性公理。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-4f940b74-b5de-43bc-8e22-502a17babe23
    field: record
    value:
      concept: tc-11c76a96-ef73-4369-9650-0f044c8eb0e7
      language: en
      id: tm-4f940b74-b5de-43bc-8e22-502a17babe23
      text: inexact equivalence
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: will-2009-skos-iso
        locator: Mapping between thesauri a–c；L131–140
        checked: '2026-09-06'
  - identity: terms/terms/tm-04654a55-fb23-444b-a74f-36f6a8793cc3
    field: record
    value:
      concept: tc-11c76a96-ef73-4369-9650-0f044c8eb0e7
      language: zh-Hans
      id: tm-04654a55-fb23-444b-a74f-36f6a8793cc3
      text: 不精确等价
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 不精确等价按Will2009明确范围判据解释；这是个人作者解释，不伪称ISO2013§11逐项核实或SKOS属性公理。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-d33a709f-8a18-4c9e-8209-9d354dce8e4b
    field: record
    value:
      concept: tc-531f3821-4ee7-4345-831e-778371f56302
      language: en
      id: tm-d33a709f-8a18-4c9e-8209-9d354dce8e4b
      text: partial equivalence
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: will-2009-skos-iso
        locator: Mapping between thesauri a–c；L131–140
        checked: '2026-09-06'
  - identity: terms/terms/tm-8065ee4d-eebb-493d-ad78-20ad9edc976e
    field: record
    value:
      concept: tc-531f3821-4ee7-4345-831e-778371f56302
      language: zh-Hans
      id: tm-8065ee4d-eebb-493d-ad78-20ad9edc976e
      text: 部分等价
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 部分等价按Will2009明确范围判据解释；这是个人作者解释，不伪称ISO2013§11逐项核实或SKOS属性公理。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-f898b175-8fa7-45c1-94ef-c548e0928757
    field: record
    value:
      concept: tc-4d6508b0-a334-4017-aa7d-205469ae902e
      language: en
      id: tm-f898b175-8fa7-45c1-94ef-c548e0928757
      text: hierarchical mapping
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: clarke-information-retrieval-thesaurus
        locator: §3.2/Figure3
        checked: '2026-09-06'
      - entity: dnb-marc-2014-05
        locator: §1 BACKGROUND，BM/NM
        checked: '2026-09-06'
  - identity: terms/terms/tm-d1c40f39-ba5d-446c-93dc-7d232d73facb
    field: record
    value:
      concept: tc-4d6508b0-a334-4017-aa7d-205469ae902e
      language: zh-Hans
      id: tm-d1c40f39-ba5d-446c-93dc-7d232d73facb
      text: 层级映射
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 层级映射保留跨词表上下位及方向；不是把ISO原未读目录冒称正文。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-d61bdf72-b103-4fd6-b4dd-75cf1bd7efdb
    field: record
    value:
      concept: tc-64b64810-6aef-4db4-b09f-aa169129c448
      language: en
      id: tm-d61bdf72-b103-4fd6-b4dd-75cf1bd7efdb
      text: associative mapping
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: clarke-information-retrieval-thesaurus
        locator: §3.2/Figure3
        checked: '2026-09-06'
      - entity: dnb-marc-2014-05
        locator: §1 BACKGROUND，RM
        checked: '2026-09-06'
  - identity: terms/terms/tm-f3dee102-5326-406c-a50e-0035c274fb25
    field: record
    value:
      concept: tc-64b64810-6aef-4db4-b09f-aa169129c448
      language: zh-Hans
      id: tm-f3dee102-5326-406c-a50e-0035c274fb25
      text: 相关映射
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 相关映射按原跨词表相关范围解释，排除等价与层级；不把RM代码新增为英文术语。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-9a48db30-ee9b-44c4-8476-fff03dcf758f
    field: record
    value:
      concept: tc-bf5e9356-ac91-49ae-9be3-8196dd66167c
      language: en
      id: tm-9a48db30-ee9b-44c4-8476-fff03dcf758f
      text: hub structure
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: zeng-interoperability
        locator: §5.2 Models of mapping process；Table2，期刊2019p.138
        checked: '2026-09-06'
  - identity: terms/terms/tm-bb2e31d0-f6c8-4913-9ed3-a7cde4cb69bd
    field: record
    value:
      concept: tc-bf5e9356-ac91-49ae-9be3-8196dd66167c
      language: zh-Hans
      id: tm-bb2e31d0-f6c8-4913-9ed3-a7cde4cb69bd
      text: 中心辐射
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 中心辐射限定参与映射结构的词表，不要求世界上所有词表或所有非中心词表互相直接映射。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-96fe4b79-c997-4371-be2c-34cffcfa045c
    field: record
    value:
      concept: tc-e340f2b4-4515-4203-b5d1-8bafee5af81a
      language: en
      id: tm-96fe4b79-c997-4371-be2c-34cffcfa045c
      text: body of knowledge
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: swebok
        locator: 官方页面Focus on Generally Accepted Knowledge；实际urllib读取
        checked: '2026-09-06'
  - identity: terms/terms/tm-4fe0093b-b34e-4012-b499-5fede4796ac8
    field: record
    value:
      concept: tc-e340f2b4-4515-4203-b5d1-8bafee5af81a
      language: en
      id: tm-4fe0093b-b34e-4012-b499-5fede4796ac8
      text: BoK
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: swebok
        locator: 官方页面Focus on Generally Accepted Knowledge；实际urllib读取
        checked: '2026-09-06'
  - identity: terms/terms/tm-7e28b4bb-070a-496c-a255-42b104a2f334
    field: record
    value:
      concept: tc-e340f2b4-4515-4203-b5d1-8bafee5af81a
      language: zh-Hans
      id: tm-7e28b4bb-070a-496c-a255-42b104a2f334
      text: 知识体系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 知识体系指知识总和，不是Guide的结构化清单；Guide仅描述其中普遍接受的部分。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-fefcd455-00ba-430b-9a70-6a62d846f22c
    field: record
    value:
      concept: tc-3945b496-c4ac-4553-81ad-4c6dab62d81c
      language: en
      id: tm-fefcd455-00ba-430b-9a70-6a62d846f22c
      text: knowledge area
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
  - identity: terms/terms/tm-886ced2e-3c75-4147-9fda-ad2d6197f9db
    field: record
    value:
      concept: tc-3945b496-c4ac-4553-81ad-4c6dab62d81c
      language: en
      id: tm-886ced2e-3c75-4147-9fda-ad2d6197f9db
      text: KA
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
  - identity: terms/terms/tm-1e9a4505-f837-4791-b088-dbf23a42b1a5
    field: record
    value:
      concept: tc-3945b496-c4ac-4553-81ad-4c6dab62d81c
      language: zh-Hans
      id: tm-1e9a4505-f837-4791-b088-dbf23a42b1a5
      text: 知识领域
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 知识领域在此限定来源模型分组，不外推出所有知识体系固定层数。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-41116f5f-b8a3-4a24-ba19-d630df03609c
    field: record
    value:
      concept: tc-89c27e71-9c5a-4e5e-a588-15c0ae59345d
      language: en
      id: tm-41116f5f-b8a3-4a24-ba19-d630df03609c
      text: knowledge unit
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
  - identity: terms/terms/tm-706fc397-2755-416b-8987-c49b655a6257
    field: record
    value:
      concept: tc-89c27e71-9c5a-4e5e-a588-15c0ae59345d
      language: en
      id: tm-706fc397-2755-416b-8987-c49b655a6257
      text: KU
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
  - identity: terms/terms/tm-30d3ded1-73eb-4069-911b-4a8c7615a2b8
    field: record
    value:
      concept: tc-89c27e71-9c5a-4e5e-a588-15c0ae59345d
      language: zh-Hans
      id: tm-30d3ded1-73eb-4069-911b-4a8c7615a2b8
      text: 知识单元
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 知识单元不仅是主题簇，补足来源明确的学习成果。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-dddee160-7342-44b8-8fe9-6eb8c6e47880
    field: record
    value:
      concept: tc-c5f9771f-7271-4128-854d-88b12df9f7ed
      language: en
      id: tm-dddee160-7342-44b8-8fe9-6eb8c6e47880
      text: topic
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: cs2023
        locator: 1.3 Introduction to Knowledge Model，Definitions and Terminology p.1
        checked: '2026-09-06'
  - identity: terms/terms/tm-58846829-6118-4a4a-b97c-8ebb5f11ede7
    field: record
    value:
      concept: tc-c5f9771f-7271-4128-854d-88b12df9f7ed
      language: zh-Hans
      id: tm-58846829-6118-4a4a-b97c-8ebb5f11ede7
      text: 主题
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 主题在本行限知识单元组成内容，核心/选修为来源课程属性，不改变本库topics层级或状态。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-192f1290-b8f5-4bc8-88e1-e9e59f3c076b
    field: record
    value:
      concept: tc-fbe9f215-a5f4-4292-92fa-b734f6c4b3ee
      language: en
      id: tm-192f1290-b8f5-4bc8-88e1-e9e59f3c076b
      text: generally accepted knowledge
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: swebok
        locator: 官方FAQ How do you define generally accepted knowledge?；实际urllib读取
        checked: '2026-09-06'
  - identity: terms/terms/tm-87f6f03d-4e23-47f5-bf01-a50df55d039e
    field: record
    value:
      concept: tc-fbe9f215-a5f4-4292-92fa-b734f6c4b3ee
      language: zh-Hans
      id: tm-87f6f03d-4e23-47f5-bf01-a50df55d039e
      text: 普遍接受的知识
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 普遍接受的知识保持SWEBOK所引PMI语境，不要求所有项目统一应用；删除全部知识体系只收此子集的旧混淆。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-b85464df-26a7-4638-91c8-5444d5bb0b22
    field: record
    value:
      concept: tc-42c4b942-41ba-486e-903d-1f2f18e37e45
      language: en
      id: tm-b85464df-26a7-4638-91c8-5444d5bb0b22
      text: Dublin Core Metadata Element Set
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: dcmi-metadata-terms
        locator: §1 Introduction；/elements/1.1十五元素集说明
        checked: '2026-09-06'
  - identity: terms/terms/tm-844d9f9e-7c57-4bcb-9f9f-434c46fd2129
    field: record
    value:
      concept: tc-42c4b942-41ba-486e-903d-1f2f18e37e45
      language: en
      id: tm-844d9f9e-7c57-4bcb-9f9f-434c46fd2129
      text: Dublin Core
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: dcmi-metadata-terms
        locator: §1 Introduction；/elements/1.1十五元素集说明
        checked: '2026-09-06'
  - identity: terms/terms/tm-e034d071-30c6-4f9d-ad39-0c283caceccf
    field: record
    value:
      concept: tc-30abb1cd-3364-4b41-a0e9-e0b8338aa348
      language: en
      id: tm-e034d071-30c6-4f9d-ad39-0c283caceccf
      text: resource
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: dcmi-metadata-terms
        locator: §1 Introduction and Definitions；资源描述语境
        checked: '2026-09-06'
  - identity: terms/terms/tm-58221260-71b0-4fe5-a010-49fa7a359bb7
    field: record
    value:
      concept: tc-30abb1cd-3364-4b41-a0e9-e0b8338aa348
      language: zh-Hans
      id: tm-58221260-71b0-4fe5-a010-49fa7a359bb7
      text: 资源
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 资源以被描述对象为范围，示例不是封闭枚举，不引入rdfs:Resource类身份。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-55467569-4a21-4fae-a9ad-ef64e59f47f3
    field: record
    value:
      concept: tc-56bf269d-a675-4fc3-a2c1-b1f38a734d81
      language: zh-Hans
      id: tm-55467569-4a21-4fae-a9ad-ef64e59f47f3
      text: 内容单元
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 内容单元继承现行项目模型与form-independence决定，不等同DITA topic；没有已确认英文形式，不补造英文。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-04fb5e11-67df-42c5-a27f-634508227d21
    field: record
    value:
      concept: tc-327c7d8a-74ac-42b2-9022-da47959a339e
      language: en
      id: tm-04fb5e11-67df-42c5-a27f-634508227d21
      text: first principle
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: aristotle-posterior-analytics-mure
        locator: BookI Part2 immediate proposition；Part3
        checked: '2026-09-06'
      - entity: aristotle-metaphysics-ross
        locator: BookI Part2/7 first principles
        checked: '2026-09-06'
  - identity: terms/terms/tm-2ef489fa-422e-4a9c-94d8-4a32b003561e
    field: record
    value:
      concept: tc-327c7d8a-74ac-42b2-9022-da47959a339e
      language: zh-Hans
      id: tm-2ef489fa-422e-4a9c-94d8-4a32b003561e
      text: 第一原理
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 第一原理保留证明起点概念，不扩大成一般拆解技巧，也不意味着不可质疑或不需认识依据。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-f5b9ffce-b288-452a-b7db-9310c5d4430d
    field: record
    value:
      concept: tc-fd033cdd-75b1-455c-9b39-431d1b9f3747
      language: en
      id: tm-f5b9ffce-b288-452a-b7db-9310c5d4430d
      text: design rationale
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: buckingham-shum-1995-design-rationale
        locator: KMI-95-14摘要首句
        checked: '2026-09-06'
  - identity: terms/terms/tm-aba00e29-f04b-459b-9fff-08488ae115a2
    field: record
    value:
      concept: tc-fd033cdd-75b1-455c-9b39-431d1b9f3747
      language: zh-Hans
      id: tm-aba00e29-f04b-459b-9fff-08488ae115a2
      text: 设计理由
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 设计理由是理由与推理的表示，不限软件架构ADR或IBIS文档格式。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-69349502-3d1e-4e46-b82f-851ba3f2360b
    field: record
    value:
      concept: tc-a64c6780-fab4-4422-86ce-d8590dae3e52
      language: en
      id: tm-69349502-3d1e-4e46-b82f-851ba3f2360b
      text: superseded
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: nygard-2011-architecture-decisions
        locator: 正文旧决定保留并mark superseded段
        checked: '2026-09-06'
  - identity: terms/terms/tm-1869ad52-b5a3-4232-bf4f-2af24209e450
    field: record
    value:
      concept: tc-a64c6780-fab4-4422-86ce-d8590dae3e52
      language: zh-Hans
      id: tm-1869ad52-b5a3-4232-bf4f-2af24209e450
      text: 被替代
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 被替代保留ADR语境；不把来源状态扩展为任意项目对象deprecated。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-c89a4642-bfe3-4c06-8fcf-ee648ef2dada
    field: record
    value:
      concept: tc-c484ee2c-a757-4f0f-9113-d2eda506c1bf
      language: en
      id: tm-c89a4642-bfe3-4c06-8fcf-ee648ef2dada
      text: content model
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: w3c-xml-1-0
        locator: §3.2.1 Element Content，允许类型/次序及重复规则
        checked: '2026-09-06'
      - entity: dita
        locator: DITA1.3 §2.6.3.1 Content models defined as entities
        checked: '2026-09-06'
  - identity: terms/terms/tm-94f6f1e0-2b90-4a19-852d-0b812a36abf6
    field: record
    value:
      concept: tc-c484ee2c-a757-4f0f-9113-d2eda506c1bf
      language: zh-Hans
      id: tm-94f6f1e0-2b90-4a19-852d-0b812a36abf6
      text: 内容模型
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 内容模型保留原SGML/DITA结构化内容语境；不换成CMS业务实体模型，原SGML来源只保留历史。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-8d5071d7-c12a-4c9c-bca1-e8c34f309cb5
    field: record
    value:
      concept: tc-c99988e5-3f77-492b-bd6e-aeca8e11ff6f
      language: en
      id: tm-8d5071d7-c12a-4c9c-bca1-e8c34f309cb5
      text: knowledge organization
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hjorland-knowledge-organization
        locator: §1 Introduction末两段，KOP与KOS
        checked: '2026-09-06'
  - identity: terms/terms/tm-2a5b2ad3-d169-488b-b6ad-2498b42dc07e
    field: record
    value:
      concept: tc-c99988e5-3f77-492b-bd6e-aeca8e11ff6f
      language: zh-Hans
      id: tm-2a5b2ad3-d169-488b-b6ad-2498b42dc07e
      text: 知识组织
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 知识组织包括过程和系统两方面；KOS只指系统，不自动与整个KO名称同义。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-6f053261-8f43-4149-b2f6-3bf771797ecf
    field: record
    value:
      concept: tc-2cc8a5dc-aa02-43fd-9cd7-f7fd9f3c3382
      language: en
      id: tm-6f053261-8f43-4149-b2f6-3bf771797ecf
      text: public figure
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: gertz-1974
        locator: 多数意见345、351–352页；一般声名/特定公共争议与发表作品反例
        checked: '2026-09-06'
  - identity: terms/terms/tm-cfe309d6-ff92-46fb-95ad-f8f58a4c3d87
    field: record
    value:
      concept: tc-2cc8a5dc-aa02-43fd-9cd7-f7fd9f3c3382
      language: zh-Hans
      id: tm-cfe309d6-ff92-46fb-95ad-f8f58a4c3d87
      text: 公众人物
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 公众人物是此美国诽谤法语境的既有中文名；作者/维护者身份不自动达到法律门槛。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-bb67e2c7-8ddc-4400-8ef4-eebad39d015a
    field: record
    value:
      concept: tc-9e03d16f-3787-4d16-9316-c46a686e0c03
      language: en
      id: tm-bb67e2c7-8ddc-4400-8ef4-eebad39d015a
      text: individual
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: owl2-primer
        locator: §3/4.1/4.7 对象、类与不同名称不保证不同个体
        checked: '2026-09-06'
  - identity: terms/terms/tm-5a9478c7-39d8-4cc8-b1b2-acfa722afe7a
    field: record
    value:
      concept: tc-9e03d16f-3787-4d16-9316-c46a686e0c03
      language: zh-Hans
      id: tm-5a9478c7-39d8-4cc8-b1b2-acfa722afe7a
      text: 个体
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 个体不限自然人；名称规范表收录是项目用法，不作为一般定义必要条件。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-d2a7e27b-39b8-46db-b043-5b4909291305
    field: record
    value:
      concept: tc-ceeab73a-dc10-4197-8bc0-8074a1eaba15
      language: en
      id: tm-d2a7e27b-39b8-46db-b043-5b4909291305
      text: partition
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: cornell-cs3110-2012-partition
        locator: Recitation14首段
        checked: '2026-09-06'
  - identity: terms/terms/tm-c8657af5-0a96-4208-a590-068abdaa6ecf
    field: record
    value:
      concept: tc-ceeab73a-dc10-4197-8bc0-8074a1eaba15
      language: zh-Hans
      id: tm-c8657af5-0a96-4208-a590-068abdaa6ecf
      text: 划分
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 划分保留集合论的非空、互斥和覆盖条件，不是磁盘分区或任意分类操作。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-9fe850d2-b2dc-47ac-a0c7-a7e2a4967744
    field: record
    value:
      concept: tc-9e701a8f-b994-4a0d-8eab-3ea769ae1b6c
      language: en
      id: tm-9fe850d2-b2dc-47ac-a0c7-a7e2a4967744
      text: genre
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iptc-genre
        locator: NewsCodes Guidelines §1.1 Descriptive NewsCodes，Genre整体说明
        checked: '2026-09-06'
  - identity: terms/terms/tm-af21a492-0a41-4c6a-aab3-9b86dd6d740d
    field: record
    value:
      concept: tc-9e701a8f-b994-4a0d-8eab-3ea769ae1b6c
      language: zh-Hans
      id: tm-af21a492-0a41-4c6a-aab3-9b86dd6d740d
      text: 体裁
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 体裁对应IPTC总体性质说明，本库genre选作者立场子集；Diátaxis需求属于另一组织依据，不作genre定义或英文同义证据。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-948869da-f697-4671-b64a-d0fcc988e012
    field: record
    value:
      concept: tc-1f71845d-b74c-4a84-84c8-3976145bd5f6
      language: en
      id: tm-948869da-f697-4671-b64a-d0fcc988e012
      text: troubleshooting
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: dita
        locator: DITA1.3 §2.7.1.6 dita-troubleshooting-topic.html首段及信息类型结构
        checked: '2026-09-06'
  - identity: terms/terms/tm-ec8494d2-3dc5-4059-88c7-c6b8cb0e7770
    field: record
    value:
      concept: tc-1f71845d-b74c-4a84-84c8-3976145bd5f6
      language: zh-Hans
      id: tm-ec8494d2-3dc5-4059-88c7-c6b8cb0e7770
      text: 排障
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 排障在原行指承载纠正信息的主题类型，不偷偷换成一般排障活动；原因与办法可未知。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-5d81868a-1cfc-4d4d-aca9-07b816ae464b
    field: record
    value:
      concept: tc-2eb24dc0-1754-4f0b-a8c9-7239f29c1943
      language: en
      id: tm-5d81868a-1cfc-4d4d-aca9-07b816ae464b
      text: tacit knowledge
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: nonaka-toyama-konno-managing-industrial-knowledge
        locator: 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式
        checked: '2026-09-06'
  - identity: terms/terms/tm-4a653060-87cf-44bb-bbad-9ef409ef92d1
    field: record
    value:
      concept: tc-2eb24dc0-1754-4f0b-a8c9-7239f29c1943
      language: zh-Hans
      id: tm-4a653060-87cf-44bb-bbad-9ef409ef92d1
      text: 隐性知识
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 隐性知识是知识管理中对应既有英文概念的行业表达；替代已读作者章节不伪称Nonaka1991原文已读。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-91d7f224-0be5-401a-8c0e-4a0abfe252f5
    field: record
    value:
      concept: tc-78034548-e62f-4b31-9921-5b22e661d1ff
      language: en
      id: tm-91d7f224-0be5-401a-8c0e-4a0abfe252f5
      text: explicit knowledge
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: nonaka-toyama-konno-managing-industrial-knowledge
        locator: 第1章，PDFp.22作者署名；PDFp.24/印刷p.16两种知识形式
        checked: '2026-09-06'
  - identity: terms/terms/tm-d140d129-94ad-47e1-9181-60fb0d66c2cb
    field: record
    value:
      concept: tc-78034548-e62f-4b31-9921-5b22e661d1ff
      language: zh-Hans
      id: tm-d140d129-94ad-47e1-9181-60fb0d66c2cb
      text: 显性知识
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 显性知识是知识管理中对应既有英文概念的行业表达；替代已读作者章节不伪称Nonaka1991原文已读。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-98076d19-5e2f-419d-82a4-353f20652a57
    field: record
    value:
      concept: tc-505c5536-a7dd-4100-999a-fe0472b66b1c
      language: en
      id: tm-98076d19-5e2f-419d-82a4-353f20652a57
      text: cheat sheet
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: american-heritage-dictionary-5-cheat-sheet
        locator: https://www.ahdictionary.com/word/search.html?q=cheat+sheet&submit.x=0&submit.y=0；Fifth Edition ©2022，cheat
          sheet义项2
        checked: '2026-09-06'
  - identity: terms/terms/tm-2923a9eb-c720-4de1-8491-c7e6665243a6
    field: record
    value:
      concept: tc-505c5536-a7dd-4100-999a-fe0472b66b1c
      language: zh-Hans
      id: tm-2923a9eb-c720-4de1-8491-c7e6665243a6
      text: 速查表
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 速查表是技术文档中cheat sheet的惯用表达；不把任何笔记集或作弊材料纳入此概念。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-a922627b-3c76-4142-ad1b-b0b38c1bab3c
    field: record
    value:
      concept: tc-066aff06-6bef-4b2d-9870-f6ff7551db7f
      language: en
      id: tm-a922627b-3c76-4142-ad1b-b0b38c1bab3c
      text: commonplace book
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: stern-fragment-whole
        locator: Tiffany Stern正文6–8段，L133–138
        checked: '2026-09-06'
  - identity: terms/terms/tm-e7af64e3-ac9e-4fbd-baaa-fecf3782cc5a
    field: record
    value:
      concept: tc-066aff06-6bef-4b2d-9870-f6ff7551db7f
      language: zh-Hans
      id: tm-e7af64e3-ac9e-4fbd-baaa-fecf3782cc5a
      text: 札记簿
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 札记簿为原中文登记，在此按主题标题组织摘录和观察的明确范围沿用；没有更强中文证据，不为换取文路径强制改为摘录簿。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-5877c07e-3cae-4a9e-9e48-d91b2ed09416
    field: record
    value:
      concept: tc-b49a8de0-d20e-42da-b7f0-f8d09ce44dc2
      language: en
      id: tm-5877c07e-3cae-4a9e-9e48-d91b2ed09416
      text: cognitive process dimension
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: krathwohl-2002-taxonomy
        locator: PDFindex2–5/印刷pp.214–217，Cognitive Process dimension及Tables2–3
        checked: '2026-09-06'
  - identity: terms/terms/tm-164f05a0-6ba3-447f-8cd9-2f1e9bf71bb3
    field: record
    value:
      concept: tc-b49a8de0-d20e-42da-b7f0-f8d09ce44dc2
      language: zh-Hans
      id: tm-164f05a0-6ba3-447f-8cd9-2f1e9bf71bb3
      text: 认知过程维度
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 认知过程维度准确对应原条目本意引用的修订版分类，不泛称理解深度；知识维度另有其义，不合并。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-06b33584-8d3e-4053-ba8d-fb7658308c79
    field: record
    value:
      concept: tc-aadb304c-3ed0-4f60-94cf-c968953d838c
      language: en
      id: tm-06b33584-8d3e-4053-ba8d-fb7658308c79
      text: governance of organizations
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-37000-2021
        locator: §3.1.1，PDFp.9/印刷p.1
        checked: '2026-09-06'
  - identity: terms/terms/tm-37d5c3fd-96dc-4d05-9676-3e7955c10f52
    field: record
    value:
      concept: tc-aadb304c-3ed0-4f60-94cf-c968953d838c
      language: en
      id: tm-37d5c3fd-96dc-4d05-9676-3e7955c10f52
      text: governance
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: iso-37000-2021
        locator: §3.1.1，PDFp.9/印刷p.1
        checked: '2026-09-06'
  - identity: terms/terms/tm-fbdc1cb5-9e94-4eaf-ba39-857028742488
    field: record
    value:
      concept: tc-aadb304c-3ed0-4f60-94cf-c968953d838c
      language: zh-Hans
      id: tm-fbdc1cb5-9e94-4eaf-ba39-857028742488
      text: 治理
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 治理保留组织层指导/监督/问责机制，不把对管理的管理概述当完整定义。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-acdb0fe2-bc90-41f2-90b0-079e9ea8d300
    field: record
    value:
      concept: tc-24c3f7b9-c6a2-4e1c-91f2-b3ee234219c8
      language: en
      id: tm-acdb0fe2-bc90-41f2-90b0-079e9ea8d300
      text: governance policy
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-37000-2021
        locator: §3.2.9，PDFp.12/印刷p.4
        checked: '2026-09-06'
  - identity: terms/terms/tm-54912589-583d-4140-88b2-e3d749a4c82f
    field: record
    value:
      concept: tc-24c3f7b9-c6a2-4e1c-91f2-b3ee234219c8
      language: zh-Hans
      id: tm-54912589-583d-4140-88b2-e3d749a4c82f
      text: 治理政策
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 治理政策补足原行治理主体限定，源词头不是一般policy；旧必须遵守的规则概述与方向定义有实质差异，需明确采纳。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-bf128cba-2cb0-4d40-ae87-74222efdc371
    field: record
    value:
      concept: tc-e61924e8-88b7-4c88-aaf2-5dad229a89ed
      language: en
      id: tm-bf128cba-2cb0-4d40-ae87-74222efdc371
      text: decision rights
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: dnd-caf-data-governance
        locator: 2022-07-28独立发表版；AppendixB data governance定义；§6.4.2 Chief Data Officer；§6.4.3.1 Data Governors
        checked: '2026-09-06'
  - identity: terms/terms/tm-641a6f25-0b53-4451-9834-f0d3ea1ce134
    field: record
    value:
      concept: tc-e61924e8-88b7-4c88-aaf2-5dad229a89ed
      language: zh-Hans
      id: tm-641a6f25-0b53-4451-9834-f0d3ea1ce134
      text: 决策权
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 决策权是作决定的权限，区别执行职责和结果问责；DND具体主体与事项提供概念对应，不冒称DAMA付费原典。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-d7c39844-82c4-4c45-ba9c-9902f7b17f51
    field: record
    value:
      concept: tc-09ff3cd6-f825-4e90-b401-4ef25c2cc084
      language: en
      id: tm-d7c39844-82c4-4c45-ba9c-9902f7b17f51
      text: monitoring
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: oecd-2024-evaluation-glossary-en-zh
        locator: Monitoring，PDFp.39，官方英文/中文对应
        checked: '2026-09-06'
  - identity: terms/terms/tm-cde84c16-a9a4-47fc-8ac3-205a5d51f1cc
    field: record
    value:
      concept: tc-09ff3cd6-f825-4e90-b401-4ef25c2cc084
      language: zh-Hans
      id: tm-cde84c16-a9a4-47fc-8ac3-205a5d51f1cc
      text: 监测
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: oecd-2024-evaluation-glossary-en-zh
        locator: Monitoring，PDFp.39，官方英文/中文对应
        checked: '2026-09-06'
  - identity: terms/terms/tm-6f0fed97-fada-4463-b83f-92193c721185
    field: record
    value:
      concept: tc-f881797d-c9ff-4f57-9523-b6a1c01c8b2c
      language: en
      id: tm-6f0fed97-fada-4463-b83f-92193c721185
      text: evaluation
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: oecd-2024-evaluation-glossary-en-zh
        locator: Evaluation，PDFp.29，官方英文/中文对应
        checked: '2026-09-06'
  - identity: terms/terms/tm-deb24ad5-acf0-4260-b259-4c50c19bca4c
    field: record
    value:
      concept: tc-f881797d-c9ff-4f57-9523-b6a1c01c8b2c
      language: zh-Hans
      id: tm-deb24ad5-acf0-4260-b259-4c50c19bca4c
      text: 评估
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: oecd-2024-evaluation-glossary-en-zh
        locator: Evaluation，PDFp.29，官方英文/中文对应
        checked: '2026-09-06'
  - identity: terms/terms/tm-f3f51b2d-e126-4c4a-a2d5-3e621f5070f5
    field: record
    value:
      concept: tc-36a1e0f4-8fe1-459a-9083-b31022a1bda1
      language: en
      id: tm-f3f51b2d-e126-4c4a-a2d5-3e621f5070f5
      text: audit trail
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: nist-sp-800-53r5
        locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；PDFp.422，AppendixA印刷p.395，audit
          trail
        checked: '2026-09-06'
  - identity: terms/terms/tm-28bdb398-c344-489c-acef-a642f04ae4d2
    field: record
    value:
      concept: tc-36a1e0f4-8fe1-459a-9083-b31022a1bda1
      language: zh-Hans
      id: tm-28bdb398-c344-489c-acef-a642f04ae4d2
      text: 审计追踪
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 审计追踪强调可重建的连续活动记录；谁/何时/何事可作为实现字段，不是全部定义。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-73cdf874-2e2b-4404-9eaf-6d0b71d41d0b
    field: record
    value:
      concept: tc-9ebb317b-d01a-4852-a71f-463f595a50a4
      language: en
      id: tm-73cdf874-2e2b-4404-9eaf-6d0b71d41d0b
      text: governance review
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: dfe-external-governance-reviews
        locator: 2026-08-11更新发表版；Benefits of an external governance review；Scope of the review
        checked: '2026-09-06'
  - identity: terms/terms/tm-f2c73c67-527c-442e-b5a7-882795cce1fc
    field: record
    value:
      concept: tc-9ebb317b-d01a-4852-a71f-463f595a50a4
      language: zh-Hans
      id: tm-f2c73c67-527c-442e-b5a7-882795cce1fc
      text: 治理评审
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 治理评审有官方实际用法；本库年度复审政策/决策权/阈值为项目实施规则，不冒称ISO37000有独立词条。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-4794e766-7ce2-4386-8b90-0c7ea06ce27a
    field: record
    value:
      concept: tc-ec453431-dede-440d-87aa-40b745fea33a
      language: en
      id: tm-4794e766-7ce2-4386-8b90-0c7ea06ce27a
      text: audit
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: nist-sp-800-53r5
        locator: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf；PDFp.422，AppendixA印刷p.395，audit
          [CNSSI4009]
        checked: '2026-09-06'
  - identity: terms/terms/tm-37aeadd2-d0a1-4a1f-9845-d3ba5b6b2b45
    field: record
    value:
      concept: tc-ec453431-dede-440d-87aa-40b745fea33a
      language: zh-Hans
      id: tm-37aeadd2-d0a1-4a1f-9845-d3ba5b6b2b45
      text: 审计
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 审计与审计追踪不同，前者是评价过程，后者是记录；原符合规则概述补足证据和准则机制。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-657b1a85-79d5-44c1-b355-f37b4e7aff07
    field: record
    value:
      concept: tc-9db2bd8b-938e-4752-865f-bec2da9c4083
      language: en
      id: tm-657b1a85-79d5-44c1-b355-f37b4e7aff07
      text: assertion
      administrative_status: preferredTerm-admn-sts
      basis:
        project:
          approval: decision-term-data-values
          origin:
            commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
            file: docs/glossary.md
            locator: 治理与维护，断言/assertion原登记
          rationale: 仅此既有英文形式的项目准入追溯；不是模型英文兜底
  - identity: terms/terms/tm-25528895-b7ab-4c59-b885-003d51cdf632
    field: record
    value:
      concept: tc-9db2bd8b-938e-4752-865f-bec2da9c4083
      language: zh-Hans
      id: tm-25528895-b7ab-4c59-b885-003d51cdf632
      text: 断言
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 断言在本条是本库限定用法，保留原名称，不扩大到所有命题断言。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-e36008bf-48ec-4391-991d-e4dc25d973e5
    field: record
    value:
      concept: tc-0aa7aa33-d7af-4c82-ad56-6efe59c4138c
      language: en
      id: tm-e36008bf-48ec-4391-991d-e4dc25d973e5
      text: indicator
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: oecd-2024-evaluation-glossary-en-zh
        locator: Indicator，PDFp.35，英文及官方中文指标紧邻
        checked: '2026-09-06'
  - identity: terms/terms/tm-e81a6d8c-836b-4599-9dd9-6487df397223
    field: record
    value:
      concept: tc-0aa7aa33-d7af-4c82-ad56-6efe59c4138c
      language: zh-Hans
      id: tm-e81a6d8c-836b-4599-9dd9-6487df397223
      text: 指标
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: oecd-2024-evaluation-glossary-en-zh
        locator: Indicator，PDFp.35，英文及官方中文指标紧邻
        checked: '2026-09-06'
  - identity: terms/terms/tm-1facfe30-6843-4a4a-989d-a7d8338cf57f
    field: record
    value:
      concept: tc-549c1bed-5db4-4073-aaab-bf23c9be47ac
      language: en
      id: tm-1facfe30-6843-4a4a-989d-a7d8338cf57f
      text: threshold
      administrative_status: preferredTerm-admn-sts
      basis:
        project:
          approval: decision-term-data-values
          origin:
            commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
            file: docs/glossary.md
            locator: 治理与维护，阈值/threshold原登记
          rationale: 仅此既有英文形式的项目登记追溯
  - identity: terms/terms/tm-f998c038-aacd-4c65-84df-c55042284579
    field: record
    value:
      concept: tc-549c1bed-5db4-4073-aaab-bf23c9be47ac
      language: zh-Hans
      id: tm-f998c038-aacd-4c65-84df-c55042284579
      text: 阈值
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 阈值保留既有指标界值用法，明确到达阈值不授予自动修改权限。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-def01f3e-50b7-4676-a941-bdda43a2dc21
    field: record
    value:
      concept: tc-ab1c42d3-59d8-49db-9aa9-eebc09a98d6c
      language: en
      id: tm-def01f3e-50b7-4676-a941-bdda43a2dc21
      text: approve
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: z39-19
        locator: §11.1.6 Candidate Terms，PDFp.105/印刷p.94；§11.4.5
        checked: '2026-09-06'
  - identity: terms/terms/tm-0abd2dc1-3755-4169-9f04-dfa271540391
    field: record
    value:
      concept: tc-ab1c42d3-59d8-49db-9aa9-eebc09a98d6c
      language: zh-Hans
      id: tm-0abd2dc1-3755-4169-9f04-dfa271540391
      text: 批准
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 批准在此是源实际approved动词语境的接受动作，不伪造独立定义号，也不从标准授予本库机器审批权。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-a3356e3f-f6c3-43bb-b088-fe607d15a8c7
    field: record
    value:
      concept: tc-4aa4867f-ea92-4a56-a56f-e8ffe45c1f91
      language: en
      id: tm-a3356e3f-f6c3-43bb-b088-fe607d15a8c7
      text: relation
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hogan-paper
        locator: arXivv6，PDFp.1 L68–88，nodes represent entities/edges represent relations
        checked: '2026-09-06'
  - identity: terms/terms/tm-d5811399-5efc-4f04-bcf1-ccea4145a933
    field: record
    value:
      concept: tc-4aa4867f-ea92-4a56-a56f-e8ffe45c1f91
      language: zh-Hans
      id: tm-d5811399-5efc-4f04-bcf1-ccea4145a933
      text: 关系
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 关系是语义联系，不是其图表示边；原relation与edge拆开，不泛化RDF predicate身份。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-b99aaec5-5d0c-4f7e-9ead-e73294328226
    field: record
    value:
      concept: tc-95d07268-89f1-4c7f-86b0-98f60eeeef52
      language: en
      id: tm-b99aaec5-5d0c-4f7e-9ead-e73294328226
      text: edge
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hogan-paper
        locator: arXivv6，PDFp.4 L192–200 directed edge-labelled graphs
        checked: '2026-09-06'
  - identity: terms/terms/tm-28070939-fa29-4c92-bfdc-f96ba6758174
    field: record
    value:
      concept: tc-95d07268-89f1-4c7f-86b0-98f60eeeef52
      language: zh-Hans
      id: tm-28070939-fa29-4c92-bfdc-f96ba6758174
      text: 边
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 边是图连接的行业名称，原定义已出现该词；作为独立中文designation本包明确提出模型第5级，不谎称旧表已经独立登记。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-f46f87b7-417d-492b-b34f-9bcb2a74fcef
    field: record
    value:
      concept: tc-daa1c79a-56f0-4d62-a360-ddaa9b332d0f
      language: en
      id: tm-f46f87b7-417d-492b-b34f-9bcb2a74fcef
      text: schema
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hogan-paper
        locator: arXivv6，PDFp.1 L84–88 high-level structure
        checked: '2026-09-06'
  - identity: terms/terms/tm-bfe84c3f-798d-441f-9306-ea6e990a168a
    field: record
    value:
      concept: tc-daa1c79a-56f0-4d62-a360-ddaa9b332d0f
      language: en
      id: tm-bfe84c3f-798d-441f-9306-ea6e990a168a
      text: Schema
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: hogan-paper
        locator: arXivv6，PDFp.1 L84–88 high-level structure
        checked: '2026-09-06'
  - identity: terms/terms/tm-e5a02701-e0ef-4995-99a9-67f4132da244
    field: record
    value:
      concept: tc-e0ddd60c-cecf-4652-8b9d-2234f194a7a1
      language: en
      id: tm-e5a02701-e0ef-4995-99a9-67f4132da244
      text: reasoning
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hogan-paper
        locator: arXivv6，§4.3 Reasoning、§4.3.1 Rules，Table6/Figure22
        checked: '2026-09-06'
  - identity: terms/terms/tm-8e2fa2f3-0729-4c4c-a8eb-bbc5df747e6e
    field: record
    value:
      concept: tc-e0ddd60c-cecf-4652-8b9d-2234f194a7a1
      language: en
      id: tm-8e2fa2f3-0729-4c4c-a8eb-bbc5df747e6e
      text: inference
      administrative_status: admittedTerm-admn-sts
      basis:
      - entity: w3c-rdf-semantics-2004
        locator: AppendixB Glossary (Informative)，Inference，L1282
        checked: '2026-09-06'
  - identity: terms/terms/tm-ac9b494f-ac60-4b34-9f0c-c1deb91ad26d
    field: record
    value:
      concept: tc-e0ddd60c-cecf-4652-8b9d-2234f194a7a1
      language: zh-Hans
      id: tm-ac9b494f-ac60-4b34-9f0c-c1deb91ad26d
      text: 推理
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 推理在此是规则或本体条件下的推导/蕴涵判定，可物化或查询重写，不必写入新边；不扩成全部归纳学习。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-53e44f07-69b0-4040-8946-8098102fb3d1
    field: record
    value:
      concept: tc-5c59be76-71b8-4e7e-8bd7-3763d8058473
      language: en
      id: tm-53e44f07-69b0-4040-8946-8098102fb3d1
      text: property graph
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: hogan-paper
        locator: arXivv6，PDFp.6 L277–328 property graphs
        checked: '2026-09-06'
  - identity: terms/terms/tm-a6977c3d-9ff1-4b1b-803b-0b604a67dacd
    field: record
    value:
      concept: tc-5c59be76-71b8-4e7e-8bd7-3763d8058473
      language: zh-Hans
      id: tm-a6977c3d-9ff1-4b1b-803b-0b604a67dacd
      text: 属性图
      administrative_status: preferredTerm-admn-sts
      basis:
        level: 5
        model:
          name: gpt-6-astra
          date: '2026-09-06'
          rationale: 属性图保留原图模型概念；Hogan已核正文支持定义，不伪称ISO39075完整条款已读。；模型知识第5级，外部中文用法未核实。
          approval: decision-term-data-values
  - identity: terms/terms/tm-7e361d24-7036-4df6-b1d1-89d2ae56c6d1
    field: record
    value:
      concept: tc-1141d95e-3a9c-4955-bb15-2e7ff25b4cf2
      language: en
      id: tm-7e361d24-7036-4df6-b1d1-89d2ae56c6d1
      text: Cypher
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: francis-et-al-2018-cypher
        locator: SIGMOD18作者稿PDFp.3/论文p.1434，§2 The Cypher Language
        checked: '2026-09-06'
  - identity: terms/terms/tm-3b963620-d52f-49e0-9c5b-3e3d9f52bcd2
    field: record
    value:
      concept: tc-5a533328-0f05-496f-b0dd-0436c4ef63b0
      language: en
      id: tm-3b963620-d52f-49e0-9c5b-3e3d9f52bcd2
      text: GQL
      administrative_status: preferredTerm-admn-sts
      basis:
      - entity: iso-39075-2024
        locator: 官方Abstract：规定用于property graphs的数据管理语言syntax与semantics；Edition1，2024-04
        checked: '2026-09-06'
- question: Q03
  resolution: recommended
  patches:
  - identity: terms/concepts/tc-56bf269d-a675-4fc3-a2c1-b1f38a734d81
    field: project_basis_scope
    value:
      concept_basis:
        project:
          approval: decision-term-data-values
          origin:
            commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
            file: docs/design/model/content-model.md
            locator: 内容单元；并参docs/decisions/form-independence.md后果
          rationale: 既有项目定义，DITA只作参考，不冒充外部同概念定义
      definitions:
      - language: zh-Hans
        text: 知识库中可独立引用、可独立标引的最小内容单位；有标题，并围绕一个主题组织。
        basis:
          project:
            approval: decision-term-data-values
            origin:
              commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
              file: docs/design/model/content-model.md
              locator: 内容单元；并参docs/decisions/form-independence.md后果
            rationale: 既有项目定义，DITA只作参考，不冒充外部同概念定义
      terms: []
  - identity: terms/concepts/tc-9db2bd8b-938e-4752-865f-bec2da9c4083
    field: project_basis_scope
    value:
      concept_basis:
        project:
          approval: decision-term-data-values
          origin:
            commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
            file: docs/design/governance/maintenance.md
            locator: 断言
          rationale: 既有本库人工赋值用法；PROV-O只支持溯源，不冒充此定义来源
      definitions:
      - language: zh-Hans
        text: 本库中由人作出判断、而不是直接抄自来源的字段值。
        basis:
          project:
            approval: decision-term-data-values
            origin:
              commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
              file: docs/design/governance/maintenance.md
              locator: 断言
            rationale: 既有本库人工赋值用法；PROV-O只支持溯源，不冒充此定义来源
      terms:
      - concept: tc-9db2bd8b-938e-4752-865f-bec2da9c4083
        language: en
        id: tm-657b1a85-79d5-44c1-b355-f37b4e7aff07
        text: assertion
        administrative_status: preferredTerm-admn-sts
        basis:
          project:
            approval: decision-term-data-values
            origin:
              commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
              file: docs/glossary.md
              locator: 治理与维护，断言/assertion原登记
            rationale: 仅此既有英文形式的项目准入追溯；不是模型英文兜底
  - identity: terms/concepts/tc-549c1bed-5db4-4073-aaab-bf23c9be47ac
    field: project_basis_scope
    value:
      concept_basis:
        project:
          approval: decision-term-data-values
          origin:
            commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
            file: docs/design/governance/maintenance.md
            locator: 阈值；触发与动作
          rationale: 现行阈值触发复核或提案，不自动批准修改
      definitions:
      - language: zh-Hans
        text: 用于判定指标何时触发复核或提案的界值。
        basis:
          project:
            approval: decision-term-data-values
            origin:
              commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
              file: docs/design/governance/maintenance.md
              locator: 阈值；触发与动作
            rationale: 现行阈值触发复核或提案，不自动批准修改
      terms:
      - concept: tc-549c1bed-5db4-4073-aaab-bf23c9be47ac
        language: en
        id: tm-1facfe30-6843-4a4a-989d-a7d8338cf57f
        text: threshold
        administrative_status: preferredTerm-admn-sts
        basis:
          project:
            approval: decision-term-data-values
            origin:
              commit: aae24737ff25cb8fbdb9ab9086b162dfb144ab81
              file: docs/glossary.md
              locator: 治理与维护，阈值/threshold原登记
            rationale: 仅此既有英文形式的项目登记追溯
- question: Q04
  resolution: recommended
  patches:
  - identity: '@control:terms'
    field: historical_designations
    value:
    - origin_id: glossary-L0021
      forms:
      - 术语表
      - 代码表
      target_concept_ids:
      - tc-94e9bdfe-cefd-445c-9a12-f276bfe75e63
      reason: 原行实际概念为NISO§5.4.1 list；术语表容易指带定义的glossary，代码表指代码及取值清单，两者不能无条件作为一般list同义名。建议采用列表；不为代码表另建code-list概念。
      display: 原称术语表／代码表，现用列表；两旧称仅供历史检索与解释，不作为此概念的准用名称。
      approval: decision-term-data-values
      disposition: withdraw_from_current_designations_of_this_concept
      effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
    - origin_id: glossary-L0061
      forms:
      - paradigmatic
      target_concept_ids:
      - tc-df2d8160-1717-4372-a38f-db96925ac980
      reason: 原单独形容词省略relationship；采用已核ISO完整名称，旧省略写法不再作独立当前designation。
      display: 原英文paradigmatic，完整名称为paradigmatic relationship。
      approval: decision-term-data-values
      disposition: replace_elliptical_adjective_with_attested_full_term
      effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
    - origin_id: glossary-L0062
      forms:
      - syntagmatic
      target_concept_ids:
      - tc-1b0b91bc-d29e-44d4-854c-cddd05aebc13
      reason: 原单独形容词未完整表示关系名称，按作者用法补足relationship。
      display: 原英文syntagmatic，完整名称为syntagmatic relationship。
      approval: decision-term-data-values
      disposition: replace_elliptical_adjective_with_attested_full_term
      effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
    - origin_id: glossary-L0192
      forms:
      - 认知层级
      - cognitive level
      target_concept_ids:
      - tc-b49a8de0-d20e-42da-b7f0-f8d09ce44dc2
      reason: Krathwohl原名称是Cognitive Process dimension，旧名称将维度简化为单一深度。作为外部概念名称建议纠正；本库level字段可选和自评用途仍按现行模型，不由名称纠正更改。
      display: 旧称认知层级／cognitive level；来源概念名称为认知过程维度／cognitive process dimension。
      approval: decision-term-data-values
      disposition: replace_inaccurate_source_designations
      effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
    - origin_id: glossary-L0200
      forms:
      - 政策
      - policy
      target_concept_ids:
      - tc-24c3f7b9-c6a2-4e1c-91f2-b3ee234219c8
      reason: 采用实际原词头governance policy与治理政策；不无条件把一般policy作为同义。旧项目政策规则的约束效力按governance文档保持，术语改名不取消实际义务。
      display: 原政策／policy在本行治理语境明确为治理政策／governance policy。
      approval: decision-term-data-values
      disposition: replace_overgeneral_designations_in_governance_context
      effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
    - origin_id: glossary-L0202
      forms:
      - 监控与评价
      - monitoring and evaluation
      target_concept_ids:
      - tc-09ff3cd6-f825-4e90-b401-4ef25c2cc084
      - tc-f881797d-c9ff-4f57-9523-b6a1c01c8b2c
      reason: 原组合是两种活动，不是一个同义名称；采用OECD已核监测/评估，旧中文组合仅保留迁移前检索，不自动作为单概念准用词。
      display: 原组合监控与评价；分别见监测（monitoring）与评估（evaluation）。
      approval: decision-term-data-values
      disposition: split_combination_and_replace_chinese_by_verified_forms
      effect: 名称处置已获采纳；现行glossary的生成与编辑源切换仍以通过统一验收后的publication为准。
---

# 术语具体值

用户于 2026-09-06 采纳[完整字段提案](../../work/reviews/2026-09-06-term-complete-candidate.md)及其[逐项值](../../work/reviews/2026-09-06-term-complete-candidate.json)。本决定采纳 157 个概念及其全部名称、定义、依据、首选／准用地位和 workflow。原 65 个概念及术语 UUID 保留，新身份来自已审阅提案，不重新分配。

## 记录与依据

完整 record patch 排除 history 字段；历史记录真实采纳与登记事件，不把提案事件当作已发生的迁移。中文模型名称保留原判断日期和理由；OECD 已核双语形式保留外部依据。三项项目定义及 assertion、threshold 两个英文形式另以同一决定中的精确 project_basis_scope 限定，不开放任意缺证回退。

六条 de-facto 定义依据须同时满足[限定定义许可](term-limited-definition-source-use.md)，完整 record 授权不能替代该许可。来源记录的字段采纳见[术语来源采纳](source-term-complete-citations.md)。

## 名称与语境

术语表／代码表、paradigmatic、syntagmatic、认知层级／cognitive level、政策／policy 及监控与评价的具体处置按 Q04 执行。退出限于这些名称作为指定概念的 designation；普通叙述、来源转录、字段标签等同文不自动构成未登记术语。当前手写 glossary 尚未由生成页替换。

Reproducible Builds 采用固定作者论文的完整环境条件，前后差异见已采纳包；本库同环境确定性不升级为跨环境可重现性或 conformance。NIST 审计与审计追踪定义分别保留系统控制与安全相关事务语境，不自动覆盖本库所有治理检查或变更记录。人员规则由[公众人物边界](person-admission-clarification.md)独立记录。

## 发布边界

本决定只采纳具体记录与形式。真实数据已登记不等于唯一编辑源已经切换；通过统一验收前不写正式 term-cutover-state，不覆盖 glossary，不启用正式消费者。publication 由主线最后核准，正式 vault、合并与发版不在本决定的执行范围。
