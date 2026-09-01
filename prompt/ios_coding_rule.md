# iOS编码规范

# 前言

车同轨，书同文。编码规范既是高效合作的基础，也是深度创新的开始。编写此编码规范的目的如下：

1. **统一开发风格，提升协作效率，让项目看起来是同一个人写的，方便快速修改别人的代码**

2. **作为代码 review 依据，不断打磨代码，使代码更健壮**

3. **为新人熟悉项目提供快速上手的抓手，迅速了解项目结构，熟悉一个模块则可以类推所有模块**

本规范参考了业界一些比较知名公司的 iOS 开发规范做了适当的修改，以更适应本公司的业务开发需求。关于开发规范部分根据约束力强弱，依次分为以下 2 类：

- 【强制】 必须遵守，违反本约定或将会引起严重的后果

- 【推荐】尽量遵守，长期遵守有助于系统稳定性和合作效率的提升

虽说一千个人眼中就有一千个哈姆雷特，但此规范更推荐全部使用【推荐】以上级别来严格要求自己，让自己的代码就像艺术品一样。

为使读者更容易理解此规范，响应规范下都对条目进行了举例说明。

1. “正例”里面举例说明了什么样的编码格式是友好的、被人喜爱的

2. “反例”里面举例说明的是什么样的编码格式是不够优雅的、让人迷惑的

> 典型的“正例”和“反例”欢迎补充👏
> 
> 

# 一、美式英语规范

【强制】 编程所使用的英语，请使用 US 英语（美式英语），因为美式英语更简洁，更符合我们日常生活中所使用的英语，而英式英语相对来说有些繁琐。可以参考如下示例：color 一词，iOS 系统控件 UIColor 使用的也是美式英语。遵循规则与 iOS 系统控件名称一致

```Plaintext
/// 正例:
UIColor *myColor = [UIColor whiteColor];
```

```Plaintext
/// 反例:
UIColor *myColour = [UIColor whiteColor];
```

# 二、代码组织结构

## 1\. 核心思想

【强制】 iOS 工程中最重要的类 `UIViewController` 中的代码组织应遵循以下规范在 ViewController 中按照不同功能划分函数，使相关功能写在一起，方便查找修改。根据功能不同，主要分为以下几个模块。如有新的无法归类的模块，则添加到懒加载后面

- ViewController 中使用 `#pragma mark - xxx` 对方法进行分隔

- 项目的生命周期应该在项目的最上部分，需要把 ViewController 所有生命周期相关的方法都放在一起

- 接下来是按钮点击事件

- 自定义公共方法

- 自定义私有方法

- 系统代理方法

- 自定义代理方法

- 懒加载

- 暂时无法归类的模块，一般都是帮助类（应该放到新的类中）

## 2\. 样例代码

```Plaintext
/// 注意事项
/// 1.pragma mark - 后面的关键字要写对，使用大驼峰命名，写成一个单词不要分开，方便搜索跳转
/// 2.核心东西尽量放到VC的上面，即Lifecycle方法，需要对外暴露的方法等
/// 3.VC尽量简洁，通用方法需要写成工具方法调用，比如加密算法、自定义弹框等，不要在VC中写，视图也应该写成子视图再引入
/// 4.生命周期中的方法，需要按照顺序添加，即按照视图加载顺序从上到下依次引入

#pragma mark - Lifecycle
- (instancetype)init {}
- (void)viewDidLoad {}
- (void)viewWillAppear:(BOOL)animated {}
- (void)didReceiveMemoryWarning {}
- (void)dealloc {}

#pragma mark - Actions
- (void)sureButtonClicked {}

#pragma mark - Public Methods
- (void)refreshUI {}

#pragma mark - Private Methods
- (void)disposeData {}

#pragma mark - UITableViewDataSource
#pragma mark - UITableViewDelegate
#pragma mark - UITextFieldDelegate
#pragma mark - CustomDelegate 

#pragma mark - Accessor
- (NSMutableArray *)dataArray {
    if (!_dataArray) {
        _dataArray = [NSMutableArray array];
    }
    return _dataArray;
}
```



# 三、命名规范

## 1\. 基本原则

【推荐】 **清晰 **，尽可能遵守 Apple 的命名约定，命名应该尽可能的清晰和简洁，但在 Objective\-C 中，清晰比简洁更重要。

1. 类名采用大驼峰（UpperCamelCase）

2. 类成员、方法小驼峰（lowerCamelCase）

3. 局部变量大小写首选小驼峰，也可使用小写下划线的形式（snake\_case）

4. C 函数的命名用大驼峰

```Plaintext
/// 正例:

/// 计算机中通用的约定俗成的缩写等，使用约定的样式，不要修改大小写
ID, URL, JSON, WWW

/// 成员变量、方法名等使用小驼峰命名
UIButton *settingsButton;
setBackgroundColor:
destinationSelection
```

```Plaintext
/// 反例:

/// 计算机中通用的约定俗成的缩写等，使用约定的样式，不要修改大小写
id, Url, json, www

/// 不要使用简写，看名称不知道是干啥用的
UIButton *setBut;
setBkgdColor:
destSel
```

## 2\. 一致性

### 1\. 命名一致

1. 【推荐】整个工程的命名风格要保持一致性，最好和苹果 SDK 的代码保持统一

2. 不同类中完成相似功能的方法应该叫一样的名字。比如我们总是用 count 来返回集合的个数，不能在 A 类中使用 count 而在 B 类中使用 getNumber

### 2\. 使用前缀

【推荐】如果代码需要打包成 Framework 给别的工程使用，或者工程项目非常庞大，需要拆分成不同的模块，使用命名前缀是非常有用的。

### 3\. 前缀事项

1. 【推荐】前缀由大写的字母缩写组成LK，比如 Cocoa 中 NS 前缀代表 NSFounation 框架中的类，IB 则代表 Interface Builder 框架。基础库用LK，平台库用LP

2. 【推荐】可以在为类、协议、函数、常量以及 typedef 宏命名的时候使用前缀，但注意不要为成员变量或者方法使用前缀，因为他们本身就包含在类的命名空间内

3. 【推荐】命名前缀的时候不要和苹果 SDK 框架冲突

## 3\. 方法名

1. 【推荐】在方法签名中，应该在方法类型\(\-/\+ 符号\)之后有一个空格。

2. 【推荐】在方法各个段之间应该也有一个空格\(符合 Apple 的风格\)。

3. 【推荐】在参数之前应该包含一个具有描述性的关键字来描述参数。

4. 【推荐】"and"这个词的用法应该保留。它不应该用于多个参数来说明，就像 initWithWidth:height 以下这个例子：

```Plaintext
/// 正例:

- (void)setExampleText:(NSString *)text image:(UIImage *)image;
- (void)sendAction:(SEL)aSelector to:(id)anObject forAllCells:(BOOL)flag;
- (id)viewWithTag:(NSInteger)tag;
- (instancetype)initWithWidth:(CGFloat)width height:(CGFloat)height;
```

```Plaintext
/// 反例:

-(void)setT:(NSString *)text i:(UIImage *)image;
- (void)sendAction:(SEL)aSelector :(id)anObject :(BOOL)flag;
- (id)taggedView:(NSInteger)tag;
- (instancetype)initWithWidth:(CGFloat)width andHeight:(CGFloat)height;
- (instancetype)initWith:(int)width and:(int)height;  // Never do this.
```



## 4\. 变量名

### 1\. 变量命名原则

【推荐】变量尽量以描述性的方式来命名。单个字符的变量命名应该尽量避免，除了在 for\(\)循环。

### 2\. 星号（\*）的使用

【推荐】在 Objective\-C 中，星号（\*）应该紧贴变量

```Plaintext
/// 正例:

NSString *text;
```

```JSON
/// 反例:

NSString* text;
NSString * text;
```

## 5\. 业务模块文件夹名

- Model 模型

- ViewModel MVVM架构的ViewModel

- View 视图

- Controller 控制器

- API 网络

- Resource/Bundle 资源

- Proxy 暴露给其他模块的接口



## 网络请求命名

命名方式以`API`结尾

```JSON
@interface LKCheckVerificationAPI : LKBusinessAPI2Manager
@end
```

# 四、语法规范

## 1\. 属性修饰符

【推荐】所有属性特性应该显式地列出来，有助于新手阅读代码。属性特性的顺序应该是 `atomic/nonatomic` 、 `strong/weak` 、 `readwrite/readonly` 。

注：原版本与在 `Interface Builder` 连接 UI 元素时自动生成代码一致。此处经过讨论及参考第三方库的写法 ，决定修改为 `atomic/nonatomic` 放在 `strong/weak` 前面，代码看起来会更清晰。

```Plaintext
/// 正例:
.h
@property (nonatomic, copy) NSString *code;
@property (nonatomic, strong) NSDictonary *dict;
@property (nonatomic, assign, readonly, getter=isIdType) BOOL idType;
@property (nonatomic, assign, readonly, getter=isNumberType) BOOL numberType;
@property (nonatomic, assign, readonly, getter=isBoolType) BOOL boolType;

/// Interface Builder 拉入的ViewController的控件直接使用即可，不需要修改
/// 注意 nonatomic 和 weak 顺序与推荐顺序不一致
@property (weak, nonatomic) IBOutlet UIView *containerView;

.m
@property (nonatomic, assign, readWrite, getter=isIdType) BOOL idType;
```

```Plaintext
/// 反例:

/// 从xib或者storyboard中拉入的控件，无需修改
@property (nonatomic, weak) IBOutlet UIView *containerView;

/// 默认的 nonatomic、strong、readwrite 不要省略
@property (nonatomic) NSString *tutorialName;
```

## 2\. 字符串使用 copy 修饰

【强制】 NSString 应该使用 copy 而不是 strong 的属性特性。为什么？即使你声明一个 NSString 的属性，有人可能传入一个 NSMutableString 的实例，然后在你没有注意的情况下修改它。

```Plaintext
/// 正例:
@property (nonatomic, copy) NSString *tutorialName;
```



```Plaintext
/// 反例:
@property (nonatomic, strong) NSString *tutorialName;
```

## 3\. 点符号语法

【推荐】点语法是一种很方便封装访问方法调用的方式。当你使用点语法时，通过使用 `getter` 或 `setter` 方法，属性被访问或修改。点语法应该总是被用来访问和修改属性，因为它使代码更加简洁。 `[]符号` 既 `方法` 更偏向于用在其他例子。应该遵循系统的使用习惯，如果是属性则使用点语法调用。例如：self\.age = 20; 是调用的 set 方法，而 person\.age = self\.age; 是调用的 get 方法

```Plaintext
/// 正例:

NSInteger arrayCount = [self.array count];
view.backgroundColor = [UIColor orangeColor];
[UIApplication sharedApplication].delegate;
```

```Plaintext
/// 反例;

NSInteger arrayCount = self.array.count;
[view setBackgroundColor:[UIColor orangeColor]];
UIApplication.sharedApplication.delegate;
```

## 4\. 常量集合

【推荐】 `NSString` 、 `NSDictionary` 、 `NSArray` 和 `NSNumber` 的字面值应该在创建这些类的不可变实例时被使用。请特别注意 `nil` 值不能传入 `NSArray` 和 `NSDictionary` 字面值，因为这样会导致 crash。不可变集合应该使用简单语法糖创建

```Plaintext
/// 正例:

NSArray *names = @[@"Brian", @"Matt", @"Chris", @"Alex", @"Steve", @"Paul"];
NSDictionary *productManagers = @{@"iPhone": @"Kate", @"iPad": @"Kamal", @"Mobile Web": @"Bill"};
NSNumber *shouldUseLiterals = @YES;
NSNumber *buildingStreetNumber = @10018;
```

```Plaintext
/// 反例:

NSArray *names = [NSArray arrayWithObjects:@"Brian", @"Matt", @"Chris", @"Alex", @"Steve", @"Paul", nil];
NSDictionary *productManagers = [NSDictionary dictionaryWithObjectsAndKeys: @"Kate", @"iPhone", @"Kamal", @"iPad", @"Bill", @"Mobile Web", nil];
NSNumber *shouldUseLiterals = [NSNumber numberWithBool:YES];
NSNumber *buildingStreetNumber = [NSNumber numberWithInteger:10018];
```

## 5\. 常量

【推荐】常量是容易重复被使用和无需通过查找和代替就能快速修改值。常量应该使用 `static` 来声明而不是使用 `#define` ，除非显式地使用宏。此处的星号（ *）使用和上面的有所不同，星号（ *）独占一个位置，不用贴近 const。

```Plaintext
/// 正例:

static NSString * const RWTAboutViewControllerCompanyName = @"RayWenderlich.com";
static CGFloat const RWTImageThumbnailHeight = 50.0;
```

```Plaintext
/// 反例:

#define CompanyName @"RayWenderlich.com"
#define thumbnailHeight 2
```

## 6\. 枚举类型

【推荐】当使用 `enum` 时，推荐使用新的固定基本类型规格，因为它有更强的类型检查和代码补全。现在 `SDK` 有一个宏 `NS_ENUM()` 来帮助和鼓励你使用固定的基本类型。

```Plaintext
/// 正例:

typedef NS_ENUM(NSInteger, RWTLeftMenuTopItemType) {
  RWTLeftMenuTopItemMain,
  RWTLeftMenuTopItemShows,
  RWTLeftMenuTopItemSchedule
};

/// 或者也可以显式地赋值
typedef NS_ENUM(NSInteger, RWTGlobalConstants) {
  RWTPinSizeMin = 1,
  RWTPinSizeMax = 5,
  RWTPinCountMin = 100,
  RWTPinCountMax = 500,
};
```



```Plaintext
/// 反例:

enum GlobalConstants {
  kMaxPinSize = 5,
  kMaxPinCount = 500,
};
```

## 7\. Case 语句

【推荐】大括号在 `case` 语句中并不是必须的，除非编译器强制要求。当一个 `case` 语句包含多行代码时，大括号应该加上。

1\. 【强制】 同一个 case 语句下，有多行代码时，需要添加大括号

```Plaintext
/// 正例:

switch (condition) {
  case 1:
    // ...
    break;
  case 2: {
    // ...
    // Multi-line example using braces
    // (多行代码时，需要使用大括号)
    break;
  }
  case 3:
    // ...
    break;
  default: 
    // ...
    break;
}
```

2\.【推荐】当相同代码被多个 case 引用时，需要添加一个注释

```Plaintext
/// 正例:

switch (condition) {
  case 1:
    // ** fall-through! **
  case 2:
    // code executed for values 1 and 2
    break;
  default: 
    // ...
    break;
}
```

## 8\. 布尔值

1\. 【强制】 在条件判断中，直接使用, `Objective-C` 中使用 `YES` 和 `NO`

```Plaintext
/// 正例:

if (someObject) {}
if (![anotherObject boolValue]) {}
```

```Plaintext
/// 反例:

if (someObject == nil) {}
if ([anotherObject boolValue] == NO) {}
if (isAwesome == YES) {} // Never do this.
if (isAwesome == true) {} // Never do this.
```

2\.【推荐】如果 `BOOL` 属性的名字是一个形容词，属性就能忽略 `is` 前缀，但要指定 `get` 访问器的惯用名称

```Plaintext
/// 正例:

@property (nonatomic, assign, getter=isEditable) BOOL editable;
```

## 9\. 条件语句

【推荐】为防止出错，主体全部添加大括号

```Plaintext
/// 正例:

if (!error) {
  return success;
}

/// 或写成一行
if (!error) return success;
```

```Plaintext
/// 反例:

if (!error)
  return success;
```

## 10\. 三元操作符

【推荐】当需要提高代码的清晰性和简洁性时，三元操作符 `?:` 才会使用。单个条件求值常常需要它。多个条件求值时，如果使用 `if` 语句或重构成实例变量时，代码会更加易读。一般来说，最好使用三元操作符是在根据条件来赋值的情况下。

```Plaintext
/// 正例:

NSInteger value = 5;
result = (value != 0) ? x : y;

BOOL isHorizontal = YES;
result = isHorizontal ? x : y;
```

```Plaintext
/// 反例:

result = a > b ? x = c > d ? c : d : y;
```

# 五、方法规范

## 1\. Init 方法

【强制】 `Init` 方法应该遵循 Apple 生成代码模板的命名规则。返回类型应该使用 `instancetype` 而不是 `id`

```Plaintext
/// 正例:

- (instancetype)init {
  self = [super init];
  if (self) {
    // ...
  }
  return self;
}
```

## 2\. 类构造方法

【强制】 当类构造方法被使用时，它应该返回类型是 `instancetype` 而不是 `id` 。这样确保编译器正确地推断结果类型。

```Plaintext
/// 正例:

@interface Airplane
+ (instancetype)airplaneWithType:(RWTAirplaneType)type;
@end
```

## 3\. CGRect 函数

【推荐】当访问 `CGRect` 里的 `x` 、 `y` 、 `width` 或 `height` 时，应该使用 `CGGeometry` 函数而不是直接通过结构体来访问。

引用 Apple 的 CGGeometry:在这个参考文档中所有的函数，接受 CGRect 结构体作为输入，在计算它们结果时隐式地标准化这些 rectangles。因此，你的应用程序应该避免直接访问和修改保存在 CGRect 数据结构中的数据。相反，使用这些函数来操纵 rectangles 和获取它们的特性。

```Plaintext
/// 正例:

CGRect frame = self.view.frame;

CGFloat x = CGRectGetMinX(frame);
CGFloat y = CGRectGetMinY(frame);
CGFloat width = CGRectGetWidth(frame);
CGFloat height = CGRectGetHeight(frame);
CGRect frame = CGRectMake(0.0, 0.0, width, height);
```

```Plaintext
/// 反例:

CGRect frame = self.view.frame;

CGFloat x = frame.origin.x;
CGFloat y = frame.origin.y;
CGFloat width = frame.size.width;
CGFloat height = frame.size.height;
CGRect frame = (CGRect){ .origin = CGPointZero, .size = frame.size };
```

## 4\. 黄金路径

【强制】 当使用条件语句时，尽量不要嵌套 if 语句，多个返回也是 ok 的减少层级，代码更简洁

```Plaintext
/// 正例:

- (void)someMethod {
  if (![someOther boolValue]) {
  return;
  }

  //Do something important
}
```

```Plaintext
/// 反例:

- (void)someMethod {
  if ([someOther boolValue]) {
    //Do something important
  }
}
```

## 5\. 错误处理

【推荐】当方法通过引用来返回一个错误参数，判断返回值而不是错误变量。

```Plaintext
/// 正例:

NSError *error;
if (![self trySomethingWithError:&error]) {
  // Handle Error
}
```

```Plaintext
/// 反例:

NSError *error;
[self trySomethingWithError:&error];
if (error) {
  // Handle Error
}
```

## 6\. 单例模式

【推荐】单例对象应该使用线程安全模式来创建共享实例。

```Plaintext
/// 正例:

+ (instancetype)sharedInstance {
  static id sharedInstance = nil;

  static dispatch_once_t onceToken;
  dispatch_once(&onceToken, ^{
    sharedInstance = [[self alloc] init];
  });

  return sharedInstance;
}
```

## 7\. 换行符

【推荐】换行符是一个很重要的主题，因为它大大的提高了可读性一行很长的代码应该分成两行代码，下一行用两个空格隔开

```Plaintext
/// 正例:
+ (void)handleCrashException:(NSString *)exceptionMessage
           exceptionCategory:(JJExceptionGuardCategory)exceptionCategory
                   extraInfo:(nullable NSDictionary *)info
```

```Plaintext
/// 反例:
+ (void)handleCrashException:(NSString *)exceptionMessage exceptionCategory:(JJExceptionGuardCategory)exceptionCategory extraInfo:(nullable NSDictionary *)info
```

## 8\. 大括号换行

【推荐】方法大括号和其他大括号 `if` 、 `else` 、 `switch` 、 `while` 等等总是在同一行语句打开但在新行中关闭。

```Plaintext
/// 正例:

if (user.isHappy) {
    //Do something
} else {
    //Do something else
}
```

```Plaintext
/// 反例:

if (user.isHappy)
{
  //Do something
}
else {
  //Do something else
}
```

## 9\. 方法换行

1. 【推荐】在方法之间应该有且只有一行，这样有利于在视觉上更清晰和更易于组织。

2. 【推荐】在方法内的空白 主要用来分离功能，但通常都抽离出来成为一个新方法。

3. 【推荐】如果一个方法有多个参数，使用冒号对齐参数，直接在每个参数后面回车就行， `Xcode` 会自动处理相应格式

4. 【推荐】如果方法中包含 `block` 参数，则应该避免以冒号对齐的方式，因为 `Xcode` 的对齐方式会让代码很难看

```Plaintext
/// 正例:

// blocks are easily readable
[UIView animateWithDuration:1.0 animations:^{
  // something
} completion:^(BOOL finished) {
  // something
}];
```

```Plaintext
/// 反例:

// colon-aligning makes the block indentation hard to read
[UIView animateWithDuration:1.0
                 animations:^{
                     // something
                 }
                 completion:^(BOOL finished) {
                     // something
                 }];
```

## 10\. 注释

【推荐】当需要注释时，注释应该用来解释这段特殊代码为什么要这样做。任何被使用的注释都必须保持最新或被删除。

一般都避免使用块注释，因为代码尽可能做到自解释，只有当断断续续或几行代码时才需要注释。



## 11\. 补充

```JSON
// 正例
//算数运算，运算符前后加空格
int a = b * c;
//三元运算
NSString *a = b ?: @""; 
NSString *a = b ? "a" : @""; 
```



# 六、路由方法名称规范

## 组件间通行路由方法

以`nativeGoto`开头，用于组件间通信。

```JSON
//私教相册分享
- (void)nativeGotoPrivateCoachAlbumShare:(NSDictionary *)params;
```

## 平台路由方法

没有任何前缀，平台路由会用户服务端下发

```JSON
//评价详情
- (void)evaluateLessonDetail:(NSDictionary *)params;
```

## 容器路由方法

以`bridgeGoto`开头，用于Magi、Wukon容器能力提供

```JSON
//打电话
- (void)bridgeGotoMakePhoneCall:(NSDictionary *)params;
```

# 七、参考链接

1. [https://github\.com/google/styleguide/blob/gh\-pages/objcguide\.md](https://xie.infoq.cn/link?target=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstyleguide%2Fblob%2Fgh-pages%2Fobjcguide.md)

2. [https://github\.com/raywenderlich/objective\-c\-style\-guide/blob/master/README\.md\#dot\-notation\-syntax](https://xie.infoq.cn/link?target=https%3A%2F%2Fgithub.com%2Fraywenderlich%2Fobjective-c-style-guide%2Fblob%2Fmaster%2FREADME.md%23dot-notation-syntax)

3. [https://github\.com/NYTimes/objective\-c\-style\-guide](https://xie.infoq.cn/link?target=https%3A%2F%2Fgithub.com%2FNYTimes%2Fobjective-c-style-guide)

4. [https://github\.com/samlaudev/Objective\-C\-Coding\-Style](https://xie.infoq.cn/link?target=https%3A%2F%2Fgithub.com%2Fsamlaudev%2FObjective-C-Coding-Style)



