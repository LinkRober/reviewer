【项目环境】
- 语言：Objective-C
- UI 框架：UIKit
- 内存管理：ARC
- 最低系统版本：iOS 13
- 架构方案：从 MVC 和 MVVM 中选择一种
- 网络层：[AFNetworking]
- 模型转换：[YYModel]
- 路由：[LPRouter]
- 响应式框架：[ReactiveObjC / RAC ]
- 布局方式：[Auto Layout / Masonry / 项目已有方案]


一、页面架构设计
如果使用 MVC：
- Model 负责数据模型和数据解析。
- View 负责布局、展示和用户输入。
- UIViewController 负责页面编排、生命周期和交互响应。
- 网络请求和复杂业务逻辑放入独立 API 或 Service 类。
- 避免将大量业务逻辑堆积在 UIViewController 中。

如果使用 MVVM：
- ViewModel 负责状态管理、数据转换和业务流程。
- ViewModel 不得依赖 UIKit。
- UIViewController 只负责生命周期、事件转发和 UI 渲染。
- 使用 Delegate、Block、RAC 或明确的 Input/Output 进行绑定。
- ViewModel 必须可以脱离 UIViewController 进行单元测试。

二、依赖检查
同一层级的模块不能横向依赖，只能通过路由的方式来调用

三、组件检查
1. 已有类似功能的组件、工具、协议不要重复创建，优先再原来的基础上迭代。相同能力不要重复实现。
2. 如果是公共组件禁止混入具体业务逻辑


四、其他
1. 只有存在项目内实现、依赖证据或明确技术影响时才报告问题。
2. 不重复报告只属于编码格式或命名风格的问题。

