export default {
	baseUrl: 'http://localhost:8080/python75f6hd0t/',
	name: '/python75f6hd0t',
	indexNav: [
		{
			name: '历年考研分数',
			url: '/index/hisyearscore',
		},
		{
			name: '公告资讯',
			url: '/index/news'
		},
		{
			name: '留言互动',
			url: '/index/messages'
		},
	],
	cateList: [
		{
			name: '公告资讯',
			refTable: 'newstype',
			refColumn: 'typename',
		},
	]
}
