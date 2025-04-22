<<<<<<< HEAD
# sql

```mysql
/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : 127.0.0.1:3306
 Source Schema         : django

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 15/06/2022 13:48:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for thread
-- ----------------------------
DROP TABLE IF EXISTS `thread`;
CREATE TABLE `thread`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `ip` char(39) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `has_enroll` tinyint(1) NOT NULL,
  `has_fee` tinyint(1) NOT NULL,
  `has_comment` tinyint(1) NOT NULL,
  `cover` varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `video` varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `photos` json NULL,
  `files` json NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `logs` json NULL,
  `auth_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `classify_id` int(11) NULL DEFAULT NULL,
  `show_id` int(11) NULL DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  `author` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_original` tinyint(1) NOT NULL,
  `price` decimal(32, 8) NULL DEFAULT NULL,
  `more` json NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `eh_thread_auth_id_4ba1b73f_fk_eh_thread_auth_id`(`auth_id`) USING BTREE,
  INDEX `eh_thread_category_id_83d71a7b_fk_eh_thread_category_id`(`category_id`) USING BTREE,
  INDEX `eh_thread_classify_id_6d669669_fk_eh_thread_classify_id`(`classify_id`) USING BTREE,
  INDEX `eh_thread_show_id_bd20d39c_fk_eh_thread_show_id`(`show_id`) USING BTREE,
  INDEX `eh_thread_title_91293eff`(`title`) USING BTREE,
  INDEX `eh_thread_user_id_9f31dde5`(`user_id`) USING BTREE,
  INDEX `eh_thread_price_e356e61e`(`price`) USING BTREE,
  CONSTRAINT `eh_thread_auth_id_4ba1b73f_fk_eh_thread_auth_id` FOREIGN KEY (`auth_id`) REFERENCES `thread_auth` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eh_thread_category_id_83d71a7b_fk_eh_thread_category_id` FOREIGN KEY (`category_id`) REFERENCES `thread_category` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eh_thread_classify_id_6d669669_fk_eh_thread_classify_id` FOREIGN KEY (`classify_id`) REFERENCES `thread_classify` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eh_thread_show_id_bd20d39c_fk_eh_thread_show_id` FOREIGN KEY (`show_id`) REFERENCES `thread_show` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 86 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_auth
-- ----------------------------
DROP TABLE IF EXISTS `thread_auth`;
CREATE TABLE `thread_auth`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_category
-- ----------------------------
DROP TABLE IF EXISTS `thread_category`;
CREATE TABLE `thread_category`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_classify
-- ----------------------------
DROP TABLE IF EXISTS `thread_classify`;
CREATE TABLE `thread_classify`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `show_id` int(11) NOT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `category_id` int(11) NULL DEFAULT NULL COMMENT '父类别',
  `icon` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '图标',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `value`(`value`) USING BTREE,
  INDEX `eh_thread_classify_show_id_65500964_fk_eh_thread_show_id`(`show_id`) USING BTREE,
  INDEX `eh_thread_classify_category_id_0001_fk_eh_thread_category_id`(`category_id`) USING BTREE,
  CONSTRAINT `eh_thread_classify_category_id_0001_fk_eh_thread_category_id` FOREIGN KEY (`category_id`) REFERENCES `thread_category` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eh_thread_classify_show_id_65500964_fk_eh_thread_show_id` FOREIGN KEY (`show_id`) REFERENCES `thread_show` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_extend_data
-- ----------------------------
DROP TABLE IF EXISTS `thread_extend_data`;
CREATE TABLE `thread_extend_data`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_1` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `field_2` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_3` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_4` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_5` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_6` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_7` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_8` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_9` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_10` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_11` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_12` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_13` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_14` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_15` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_16` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_17` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_18` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_19` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `field_20` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `thread_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `eh_thread_extend_data_thread_id_89eebd4a_fk_eh_thread_id`(`thread_id`) USING BTREE,
  CONSTRAINT `eh_thread_extend_data_thread_id_89eebd4a_fk_eh_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `thread` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_extend_field
-- ----------------------------
DROP TABLE IF EXISTS `thread_extend_field`;
CREATE TABLE `thread_extend_field`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `unit` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `classify_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `eh_thread_extend_field_classify_id_field_537821d6_uniq`(`classify_id`, `field`) USING BTREE,
  CONSTRAINT `eh_thread_extend_fie_classify_id_b341a273_fk_eh_thread` FOREIGN KEY (`classify_id`) REFERENCES `thread_classify` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_image_auth
-- ----------------------------
DROP TABLE IF EXISTS `thread_image_auth`;
CREATE TABLE `thread_image_auth`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_resource
-- ----------------------------
DROP TABLE IF EXISTS `thread_resource`;
CREATE TABLE `thread_resource`  (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `url` varchar(1024) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `filename` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `filetype` smallint(6) NULL DEFAULT NULL,
  `format` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `price` decimal(32, 8) NULL DEFAULT NULL,
  `snapshot` json NULL,
  `logs` json NULL,
  `image_auth_id` int(11) NULL DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `eh_thread_resource_user_id_647f8542_fk_mz_user_id`(`user_id`) USING BTREE,
  INDEX `eh_thread_resource_image_auth_id_2662cb84_fk_eh_thread`(`image_auth_id`) USING BTREE,
  INDEX `eh_thread_resource_price_9bc424eb`(`price`) USING BTREE,
  CONSTRAINT `eh_thread_resource_image_auth_id_2662cb84_fk_eh_thread` FOREIGN KEY (`image_auth_id`) REFERENCES `thread_image_auth` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_show
-- ----------------------------
DROP TABLE IF EXISTS `thread_show`;
CREATE TABLE `thread_show`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `config` json NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT ' ',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_statistic
-- ----------------------------
DROP TABLE IF EXISTS `thread_statistic`;
CREATE TABLE `thread_statistic`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `flag_classifies` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `flag_weights` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `weight` double NOT NULL,
  `views` int(11) NOT NULL,
  `plays` int(11) NOT NULL,
  `comments` int(11) NOT NULL,
  `likes` int(11) NOT NULL,
  `favorite` int(11) NOT NULL,
  `shares` int(11) NOT NULL,
  `thread_id_id` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `thread_id_id`(`thread_id_id`) USING BTREE,
  INDEX `eh_thread_statistic_weight_3752b28a`(`weight`) USING BTREE,
  CONSTRAINT `eh_thread_statistic_thread_id_id_7763ffcc_fk_eh_thread_id` FOREIGN KEY (`thread_id_id`) REFERENCES `thread` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 44 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_tag
-- ----------------------------
DROP TABLE IF EXISTS `thread_tag`;
CREATE TABLE `thread_tag`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_tag_mapping
-- ----------------------------
DROP TABLE IF EXISTS `thread_tag_mapping`;
CREATE TABLE `thread_tag_mapping`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_id` int(11) NOT NULL,
  `thread_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `eh_thread_tag_mapping_tag_id_0e339c9b_fk_eh_thread_tag_id`(`tag_id`) USING BTREE,
  INDEX `eh_thread_tag_mapping_thread_id_eceb96e8_fk_eh_thread_id`(`thread_id`) USING BTREE,
  CONSTRAINT `eh_thread_tag_mapping_tag_id_0e339c9b_fk_eh_thread_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `thread_tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eh_thread_tag_mapping_thread_id_eceb96e8_fk_eh_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `thread` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_to_resource
-- ----------------------------
DROP TABLE IF EXISTS `thread_to_resource`;
CREATE TABLE `thread_to_resource`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `resource_id` bigint(20) NOT NULL,
  `thread_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `eh_thread_to_resourc_resource_id_ab2eab84_fk_eh_thread`(`resource_id`) USING BTREE,
  INDEX `eh_thread_to_resource_thread_id_9d5d277d_fk_eh_thread_id`(`thread_id`) USING BTREE,
  CONSTRAINT `eh_thread_to_resourc_resource_id_ab2eab84_fk_eh_thread` FOREIGN KEY (`resource_id`) REFERENCES `thread_resource` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eh_thread_to_resource_thread_id_9d5d277d_fk_eh_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `thread` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_transact
-- ----------------------------
DROP TABLE IF EXISTS `thread_transact`;
CREATE TABLE `thread_transact`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `amount` decimal(32, 2) NOT NULL,
  `balance` decimal(32, 2) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `remark` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `snapshot` json NULL,
  `currency_id` int(11) NOT NULL,
  `pay_mode_id` int(11) NOT NULL,
  `thread_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `eh_transact_currency_id_a6ec55bb_fk_eh_transact_currency_id`(`currency_id`) USING BTREE,
  INDEX `eh_transact_pay_mode_id_3ca69012_fk_eh_transact_paymode_id`(`pay_mode_id`) USING BTREE,
  INDEX `eh_transact_thread_id_f492b164_fk_eh_thread_id`(`thread_id`) USING BTREE,
  INDEX `eh_transact_user_id_7723fcf3_fk_mz_user_id`(`user_id`) USING BTREE,
  INDEX `eh_transact_amount_a5ca65d2`(`amount`) USING BTREE,
  INDEX `eh_transact_balance_18c9a594`(`balance`) USING BTREE,
  CONSTRAINT `eh_transact_currency_id_a6ec55bb_fk_eh_transact_currency_id` FOREIGN KEY (`currency_id`) REFERENCES `thread_transact_currency` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eh_transact_pay_mode_id_3ca69012_fk_eh_transact_paymode_id` FOREIGN KEY (`pay_mode_id`) REFERENCES `thread_transact_paymode` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eh_transact_thread_id_f492b164_fk_eh_thread_id` FOREIGN KEY (`thread_id`) REFERENCES `thread` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `eh_transact_user_id_7723fcf3_fk_mz_user_id` FOREIGN KEY (`user_id`) REFERENCES `del_mz_user_v3` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_transact_currency
-- ----------------------------
DROP TABLE IF EXISTS `thread_transact_currency`;
CREATE TABLE `thread_transact_currency`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_virtual` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for thread_transact_paymode
-- ----------------------------
DROP TABLE IF EXISTS `thread_transact_paymode`;
CREATE TABLE `thread_transact_paymode`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

```

# 使用

1.在API中有部分耦合，需要调用用户信息的需要使用：

```python
from .utils.custom_authentication_wrapper import authentication_wrapper

@authentication_wrapper
fun.....


# 或者
from apps.user.utils.custom_authorization import CustomAuthentication
class ShowListAPIView(APIView):
    """
    get:展示类型列表
    """
    authentication_classes = (CustomAuthentication,)

    def get(self, request, *args, **kwargs):
        res = t.thread_show(request)
        return res

```



# 富文本编辑器的使用：

富文本编辑器，在web开发中可以说是不可缺少的。django并没有自带富文本编辑器，因此我们需要自己集成，在这里推荐大家使用DjangoUeditor，因为DjangoUeditor封装了我们需要的一些功能如文件上传、在后台和前台一起使用等，非常方便。

#### 一、下载DjangoUeditor:

​        1.python3: https://github.com/twz915/DjangoUeditor3/ (直接下载zip)
​        2.python2:https://github.com/zhangfisher/DjangoUeditor(直接下载zip,或 pip install DjangoUeditor)

#### 二、 新建django项目:

​        1. 在项目的根目录新建extra_apps文件夹并将我们下载好的zip文件解压打开后找到 DjangoUeditor将DjangoUeditor直接拷贝到我们项目的extra_apps中
​        2.在settings.py文件中添加两行代码：如下
​              sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
​              sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
​        3.变成蓝色文件夹后就可以在settings.py 的INSTALLED_APPS中引入DjangoUeditor
PS：注意如果反向代理访问需要再次执行一次，防止样式失效。 python  mananger.py  collectstatic

#### 三、异常处理：报错：ModuleNotFoundError: No module named 'django.utils.six' 的解决办法

报错原因：在python高版本，由于缺少six.py，会导致DjangoUeditor模块无法找到`'django.utils.six'`模块

解决办法：如果是虚拟机，将venv/Lib/site-packages/six.py文件拷贝到venv/Lib/site-packages/django/utils/six.py即可解决



# 版本差别：

v2保持原有接口，但是支持扩展字段配置，扩展字段增删改查。但是还没有做条件搜索
=======
# xj-thread

#### 介绍
{**以下是 Gitee 平台说明，您可以替换此简介**
Gitee 是 OSCHINA 推出的基于 Git 的代码托管平台（同时支持 SVN）。专为开发者提供稳定、高效、安全的云端软件开发协作平台
无论是个人、团队、或是企业，都能够用 Gitee 实现代码托管、项目管理、协作开发。企业项目请看 [https://gitee.com/enterprises](https://gitee.com/enterprises)}

#### 软件架构
软件架构说明


#### 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

#### 使用说明

1.  xxxx
2.  xxxx
3.  xxxx

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
>>>>>>> remotes/origin/master
