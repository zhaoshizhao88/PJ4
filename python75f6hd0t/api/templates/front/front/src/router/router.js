import VueRouter from 'vue-router'
//引入组件
import Index from '../pages'
import Home from '../pages/home/home'
import Login from '../pages/login/login'
import Register from '../pages/register/register'
import Center from '../pages/center/center'
import Messages from '../pages/messages/list'
import Storeup from '../pages/storeup/list'
import News from '../pages/news/news-list'
import NewsDetail from '../pages/news/news-detail'
import payList from '../pages/pay'

import hisyearscoreList from '../pages/hisyearscore/list'
import hisyearscoreDetail from '../pages/hisyearscore/detail'
import hisyearscoreAdd from '../pages/hisyearscore/add'
import yonghuList from '../pages/yonghu/list'
import yonghuDetail from '../pages/yonghu/detail'
import yonghuAdd from '../pages/yonghu/add'
import kaoyanyixiangList from '../pages/kaoyanyixiang/list'
import kaoyanyixiangDetail from '../pages/kaoyanyixiang/detail'
import kaoyanyixiangAdd from '../pages/kaoyanyixiang/add'
import tuijianyuanxiaoList from '../pages/tuijianyuanxiao/list'
import tuijianyuanxiaoDetail from '../pages/tuijianyuanxiao/detail'
import tuijianyuanxiaoAdd from '../pages/tuijianyuanxiao/add'
import syslogList from '../pages/syslog/list'
import syslogDetail from '../pages/syslog/detail'
import syslogAdd from '../pages/syslog/add'
import newstypeList from '../pages/newstype/list'
import newstypeDetail from '../pages/newstype/detail'
import newstypeAdd from '../pages/newstype/add'
import discusshisyearscoreList from '../pages/discusshisyearscore/list'
import discusshisyearscoreDetail from '../pages/discusshisyearscore/detail'
import discusshisyearscoreAdd from '../pages/discusshisyearscore/add'

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => err)
}

//配置路由
export default new VueRouter({
	routes:[
		{
      path: '/',
      redirect: '/index/home'
    },
		{
			path: '/index',
			component: Index,
			children:[
				{
					path: 'home',
					component: Home
				},
				{
					path: 'center',
					component: Center,
				},
				{
					path: 'pay',
					component: payList,
				},
				{
					path: 'messages',
					component: Messages
				},
				{
					path: 'storeup',
					component: Storeup
				},
				{
					path: 'news',
					component: News
				},
				{
					path: 'newsDetail',
					component: NewsDetail
				},
				{
					path: 'hisyearscore',
					component: hisyearscoreList
				},
				{
					path: 'hisyearscoreDetail',
					component: hisyearscoreDetail
				},
				{
					path: 'hisyearscoreAdd',
					component: hisyearscoreAdd
				},
				{
					path: 'yonghu',
					component: yonghuList
				},
				{
					path: 'yonghuDetail',
					component: yonghuDetail
				},
				{
					path: 'yonghuAdd',
					component: yonghuAdd
				},
				{
					path: 'kaoyanyixiang',
					component: kaoyanyixiangList
				},
				{
					path: 'kaoyanyixiangDetail',
					component: kaoyanyixiangDetail
				},
				{
					path: 'kaoyanyixiangAdd',
					component: kaoyanyixiangAdd
				},
				{
					path: 'tuijianyuanxiao',
					component: tuijianyuanxiaoList
				},
				{
					path: 'tuijianyuanxiaoDetail',
					component: tuijianyuanxiaoDetail
				},
				{
					path: 'tuijianyuanxiaoAdd',
					component: tuijianyuanxiaoAdd
				},
				{
					path: 'syslog',
					component: syslogList
				},
				{
					path: 'syslogDetail',
					component: syslogDetail
				},
				{
					path: 'syslogAdd',
					component: syslogAdd
				},
				{
					path: 'newstype',
					component: newstypeList
				},
				{
					path: 'newstypeDetail',
					component: newstypeDetail
				},
				{
					path: 'newstypeAdd',
					component: newstypeAdd
				},
				{
					path: 'discusshisyearscore',
					component: discusshisyearscoreList
				},
				{
					path: 'discusshisyearscoreDetail',
					component: discusshisyearscoreDetail
				},
				{
					path: 'discusshisyearscoreAdd',
					component: discusshisyearscoreAdd
				},
			]
		},
		{
			path: '/login',
			component: Login
		},
		{
			path: '/register',
			component: Register
		},
	]
})
