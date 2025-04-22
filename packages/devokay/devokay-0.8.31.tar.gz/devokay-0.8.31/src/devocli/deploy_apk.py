


def cmd_handle_latest(args):
    # fir = FirIM(args.token)
    # fir.get_latest_ver(args.app_id)
    pass

# 一键上传apk到应用商店，支持小米市场，vivo市场，huawei市场
# https://github.com/lianaini/market_upload

'''
    a. 小米
    b. 华为
    c. 应用宝
    d. 百度
    e. 360
    f. oppo
    g. vivo
'''
def cmd_regist(subparsers):
    parser = subparsers.add_parser('deploy.apk.tecent', help='fir get latest version info')
    parser.set_defaults(handle=cmd_handle_latest)

    parser = subparsers.add_parser('deploy.apk.xiaomi', help='fir upload build file')
    parser.set_defaults(handle=cmd_handle_latest)

    parser = subparsers.add_parser('deploy.apk.yingyongbao', help='fir upload build file')
    parser.set_defaults(handle=cmd_handle_latest)

    parser = subparsers.add_parser('deploy.apk.baidu', help='fir get latest version info')
    parser.set_defaults(handle=cmd_handle_latest)

    parser = subparsers.add_parser('deploy.apk.360', help='fir upload build file')
    parser.set_defaults(handle=cmd_handle_latest)

    parser = subparsers.add_parser('deploy.apk.oppo', help='fir get latest version info')
    parser.set_defaults(handle=cmd_handle_latest)

    parser = subparsers.add_parser('deploy.apk.vivo', help='fir get latest version info')
    parser.set_defaults(handle=cmd_handle_latest)

    parser = subparsers.add_parser('deploy.apk.google', help='fir get latest version info')
    parser.set_defaults(handle=cmd_handle_latest)


'''
1. 腾讯应用宝
1.1 Tencent MyApp App Store
1.2 android.myapp.com
1.3 月活 0.27 亿

2. oppo软件商店
2.1 Oppo App Store
2.2 https://store.oppomobile.com
2.3 1.25

3. 华为应用市场
3.1 Huawei App Store
3.2 https://app.hicloud.com
3.3 1.22

4. 360手机助手
4.1 360 Mobile Assistant
4.2 zhushou.360.cn
4.3 1.02

5. 小米应用商店
5.1 Xiaomi App Store
5.2 app.xiaomi.com
5.3 8700

6. 百度手机助手
6.1 Baidu Mobile Assistant
6.2 as.baidu.com
6.3 8100

7. vivo应用商店
7.1 VIVO App Store
7.2 dev.vivo.com.cn/distrib
7.4 6900

8. PP助手
8.1 PP Assistant
8.2 https://25pp.com
8.3 2500

9. 中国移动MM商店
9.1 China Mobile MM Store
9.2 mm.10086.cn/store
9.3 2500

10. 安智市场
10.1 Anzhi Market
10.2 anzhi.com/applist/html
10.3 2500

'''