fs = require 'fs'
r = require 'request'
async = require 'async'
# $ = require 'jquery'
# {env} = require 'jsdom'

s = fs.readFileSync 'mingdao_api_description.json', 'utf8'
o = JSON.parse s

urls = 
	'post/followed': 'http://open.mingdao.com/post/post-followed.html'
	'post/all': 'http://open.mingdao.com/post/post-all.html'
	'post/my': 'http://open.mingdao.com/post/post-my.html'
	'post/atme': 'http://open.mingdao.com/post/post-atme.html'
	'post/atme_2': 'http://open.mingdao.com/post/post-atme_2.html'
	'post/replybyme': 'http://open.mingdao.com/post/post-replybyme.html'
	'post/replyme': 'http://open.mingdao.com/post/post-replyme.html'
	'post/favorite': 'http://open.mingdao.com/post/post-favorite.html'
	'post/group': 'http://open.mingdao.com/post/post-group.html'
	'post/user': 'http://open.mingdao.com/post/post-user.html'
	'post/doc': 'http://open.mingdao.com/post/post-doc.html'
	'post/img': 'http://open.mingdao.com/post/post-img.html'
	'post/faq': 'http://open.mingdao.com/post/post-faq.html'
	'post/list_toppost': 'http://open.mingdao.com/post/post-list_toppost.html'
	'post/unreadcount': 'http://open.mingdao.com/post/post-unreadcount.html'
	'post/unreadatmecount': 'http://open.mingdao.com/post/post_unreadatmecount.htm'
	'post/unreadreplymecount': 'http://open.mingdao.com/post/post_unreadreplymecount.htm'
	'post/detail': 'http://open.mingdao.com/post/post-detail.html'
	'post/reply': 'http://open.mingdao.com/post/post-reply.html'
	'post/qa_thebestcomment': 'http://open.mingdao.com/post/post-qa_thebestcomment.html'
	'post/update': 'http://open.mingdao.com/post/post-update.html'
	'post/upload': 'http://open.mingdao.com/post/post-upload.html'
	'post/edit': 'http://open.mingdao.com/post/post-edit.html'
	'post/top_post': 'http://open.mingdao.com/post/post-top_post.html'
	'post/delete': 'http://open.mingdao.com/post/post-delete.html'
	'post/repost': 'http://open.mingdao.com/post/post-repost.html'
	'post/add_reply': 'http://open.mingdao.com/post/post-add_reply.html'
	'post/delete_reply': 'http://open.mingdao.com/post/post-delete_reply.html'
	'post/add_favorite': 'http://open.mingdao.com/post/post-add_favorite.html'
	'post/delete_favorite': 'http://open.mingdao.com/post/post-delete_favorite.html'
	'post/add_like': 'http://open.mingdao.com/post/post-add_like.html'
	'post/delete_like': 'http://open.mingdao.com/post/post-delete_like.html'
	'post/list_tag': 'http://open.mingdao.com/post/post_list_tag.html'
	'post/tag': 'http://open.mingdao.com/post/post_tag.html'
	'post/add_tag': 'http://open.mingdao.com/post/post_add_tag.html'
	'post/delete_tag': 'http://open.mingdao.com/post/post_delete_tag.html'
	'post/set_bestcomment': 'http://open.mingdao.com/post/post-set_bestcomment.html'
	'post/remove_center': 'http://open.mingdao.com/post/post-remove_center.html'
	'vote/my_joined': 'http://open.mingdao.com/vote/vote_my_joined.html'
	'vote/my_create': 'http://open.mingdao.com/vote/vote_my_create.html'
	'vote/all': 'http://open.mingdao.com/vote/vote_all.html'
	'vote/detail': 'http://open.mingdao.com/vote/vote_detail.html'
	'vote/cast_options': 'http://open.mingdao.com/vote/vote_cast_options.html'
	'vote/create': 'http://open.mingdao.com/vote/vote_create.html'
	'task/my_joined': 'http://open.mingdao.com/task/task-my_joined.html'
	'task/my_joined_finished': 'http://open.mingdao.com/task/task-my_joined_finished.html'
	'task/my_assign': 'http://open.mingdao.com/task/task-my_assign.html'
	'task/my_assign_finished': 'http://open.mingdao.com/task/task-my_assign_finished.html'
	'task/my_charge': 'http://open.mingdao.com/task/task-my_charge.html'
	'task/my_charge_finished': 'http://open.mingdao.com/task/task-my_charge_finished.html'
	'task/my_observer': 'http://open.mingdao.com/task/task-my_observer.html'
	'task/my_observer_finished': 'http://open.mingdao.com/task/task-my_observer_finished.html'
	'task/project': 'http://open.mingdao.com/task/task-project.html'
	'task/unreadcount': 'http://open.mingdao.com/task/task-unreadcount.html'
	'task/detail': 'http://open.mingdao.com/task/task-detail.html'
	'task/reply': 'http://open.mingdao.com/task/task-reply.html'
	'task/create': 'http://open.mingdao.com/task/task-create.html'
	'task/add_project': 'http://open.mingdao.com/task/task_add_project.html'
	'task/edit_folder': 'http://open.mingdao.com/task/task_edit_folder.html'
	'task/delete_folder': 'http://open.mingdao.com/task/task_delete_folder.html'
	'task/edit_title': 'http://open.mingdao.com/task/task_edit_title.html'
	'task/edit_des': 'http://open.mingdao.com/task/task_edit_des.html'
	'task/edit_charge': 'http://open.mingdao.com/task/task_edit_charge.html'
	'task/edit_expiredate': 'http://open.mingdao.com/task/task_edit_expiredate.html'
	'task/edit_project': 'http://open.mingdao.com/task/task_edit_project.html'
	'task/add_member': 'http://open.mingdao.com/task/task_add_member.html'
	'task/delete_member': 'http://open.mingdao.com/task/task_delete_member.html'
	'task/finish': 'http://open.mingdao.com/task/task-finish.html'
	'task/unfinish': 'http://open.mingdao.com/task/task_unfinish.html'
	'task/apply_observer': 'http://open.mingdao.com/task/task-apply_observer.html'
	'task/add_observer': 'http://open.mingdao.com/task/task-add_observer.html'
	'task/addreply': 'http://open.mingdao.com/task/task-addreply.html'
	'task/delete': 'http://open.mingdao.com/task/task-delete.html'
	'task/delete_topic': 'http://open.mingdao.com/task/task_delete_topic.html'
	'task/edit_priority': 'http://open.mingdao.com/task/task_edit_priority.html'
	'task/add_topic_bypost': 'http://open.mingdao.com/task/task_add_topic_bypost.html'
	'task/duplicate_task': 'http://open.mingdao.com/task/task_duplicate_task.html'
	'calendar/todo': 'http://open.mingdao.com/calendar/calendar_todo.html'
	'calendar/day': 'http://open.mingdao.com/calendar/calendar_day.html'
	'calendar/week': 'http://open.mingdao.com/calendar/calendar_week.html'
	'calendar/month': 'http://open.mingdao.com/calendar/calendar_month.html'
	'calendar/detail': 'http://open.mingdao.com/calendar/calendar_detail.html'
	'calendar/create': 'http://open.mingdao.com/calendar/calendar_create.html'
	'calendar/edit': 'http://open.mingdao.com/calendar/calendar_edit.html'
	'calendar/add_member': 'http://open.mingdao.com/calendar/calendar_add_member.html'
	'calendar/delete_member': 'http://open.mingdao.com/calendar/calendar_delete_member.html'
	'calendar/exit': 'http://open.mingdao.com/calendar/calendar_exit.html'
	'calendar/join': 'http://open.mingdao.com/calendar/calendar_join.html'
	'calendar/deny': 'http://open.mingdao.com/calendar/calendar_deny.html'
	'calendar/reinvite_member': 'http://open.mingdao.com/calendar/calendar_reinvite_member.html'
	'calendar/destroy': 'http://open.mingdao.com/calendar/calendar_delete.html'
	'user/all': 'http://open.mingdao.com/user/user-all.html'
	'user/search': 'http://open.mingdao.com/user/user-search.html'
	'user/detail': 'http://open.mingdao.com/user/user-detail.html'
	'user/followed': 'http://open.mingdao.com/user/user-followed.html'
	'user/list': 'http://open.mingdao.com/user/user-list.html'
	'user/get_managerUser': 'http://open.mingdao.com/user/user-get_managerUser.html'
	'user/get_managerUserTree': 'http://open.mingdao.com/user/user-get_managerUserTree.html'
	'user/department': 'http://open.mingdao.com/user/user-department.html'
	'user/work_site': 'http://open.mingdao.com/user/user-work_site.html'
	'user/add_followed': 'http://open.mingdao.com/user/user-add_followed.html'
	'user/delete_followed': 'http://open.mingdao.com/user/user-delete_followed.html'
	'user/invite': 'http://open.mingdao.com/user/user-invite.html'
	'user/frequent': 'http://open.mingdao.com/user/user_frequent.htm'
	'user/add_frequent': 'http://open.mingdao.com/user/user_add_frequent.htm'
	'user/delete_frequent': 'http://open.mingdao.com/user/user_delete_frequent.htm'
	'user/find_password': 'http://open.mingdao.com/user/find_password.html'
	'invite/invited_user': 'http://open.mingdao.com/invite/invite-invited_user.html'
	'invite/again_inviteuser': 'http://open.mingdao.com/invite/invite-again_inviteuser.html'
	'invite/close_inviteuser': 'http://open.mingdao.com/invite/invite-close_inviteuser.html'
	'group/all': 'http://open.mingdao.com/group/group-all.html'
	'group/detail': 'http://open.mingdao.com/group/group-detail.html'
	'group/my_created': 'http://open.mingdao.com/group/group-my_created.html'
	'group/my_joined': 'http://open.mingdao.com/group/group-my_joined.html'
	'group/user': 'http://open.mingdao.com/group/group-user.html'
	'group/create': 'http://open.mingdao.com/group/group-create.html'
	'group/exit': 'http://open.mingdao.com/group/group-exit_join_close_open_delete.html'
	'group/join': 'http://open.mingdao.com/group/group-exit_join_close_open_delete.html'
	'group/close': 'http://open.mingdao.com/group/group-exit_join_close_open_delete.html'
	'group/open': 'http://open.mingdao.com/group/group-exit_join_close_open_delete.html'
	'group/delete': 'http://open.mingdao.com/group/group-exit_join_close_open_delete.html'
	'group/invite': 'http://open.mingdao.com/group/group-invite.html'
	'group/add_admin': 'http://open.mingdao.com/group/group-add_admin.html'
	'group/remove_user': 'http://open.mingdao.com/group/group-remove_user.html'
	'group/remove_admin': 'http://open.mingdao.com/group/group-remove_admin.html'
	'groupinvite/invited_user': 'http://open.mingdao.com/groupinvite/groupinvite-invited_user.html'
	'groupinvite/again_inviteuser': 'http://open.mingdao.com/groupinvite/groupinvite-again_inviteuser.html'
	'groupinvite/close_inviteuser': 'http://open.mingdao.com/groupinvite/groupinvite-close_inviteuser.html'
	'message/all': 'http://open.mingdao.com/message/message-all.html'
	'message/list': 'http://open.mingdao.com/message/message-list.html'
	'message/unreadcount': 'http://open.mingdao.com/message/message-unreadcount.html'
	'message/create': 'http://open.mingdao.com/message/message-create.html'
	'message/create_sys': 'http://open.mingdao.com/message/message-create_sys.html'
	'message/read': 'http://open.mingdao.com/message/message-read.html'
	'passport/detail': 'http://open.mingdao.com/passport/passport-detail.html'
	'passport/get_setting': 'http://open.mingdao.com/passport/passport-get_setting.html'
	'passport/unreadcount': 'http://open.mingdao.com/passport/passport-unreadcount.html'
	'passport/edit': 'http://open.mingdao.com/passport/passport-edit.html'
	'passport/edit_avstar': 'http://open.mingdao.com/passport/passport-edit_avstar.html'
	'passport/logout': 'http://open.mingdao.com/passport/passport-logout.html'
	'passport/setuserpush': 'http://open.mingdao.com/passport/passport_setuserpush.htm'
	'company/detail': 'http://open.mingdao.com/company/company_detail.html'
	'company/get_setting': 'http://open.mingdao.com/company/company-get_setting.html'
	'company/get_admin': 'http://open.mingdao.com/company/company_get_admin.html'
	'company/add_admin': 'http://open.mingdao.com/company/company_add_admin.html'
	'company/delete_admin': 'http://open.mingdao.com/company/company_delete_admin.html'
	'company/is_admin': 'http://open.mingdao.com/company/company_is_admin.html'
	'user/close_user': 'http://open.mingdao.com/user/user_close_user.htm'
	'user/remove_user': 'http://open.mingdao.com/user/user_remove_user.htm'
	'app/version': 'http://open.mingdao.com/app/app_version.html'
	'app/get_admin': 'http://open.mingdao.com/app/app_get_admin.html'
	'app/get_applist': 'http://open.mingdao.com/app/app_get_applist.html'
	'app/add_admin': 'http://open.mingdao.com/app/app_add_admin.html'
	'app/delete_admin': 'http://open.mingdao.com/app/app_delete_admin.html'
	'app/statistics': 'http://open.mingdao.com/app/app_statistics.html'
	'app/is_admin': 'http://open.mingdao.com/app/app_is_admin.html'
	'app/app_addAppNotice': 'http://open.mingdao.com/app/app_addAppNotice.html'
	'app/app_readAppNotice': 'http://open.mingdao.com/app/app_readAppNotice.html'
	'oauth2/authorize': 'http://open.mingdao.com/oauth2/oauth2-authorize.html'
	'oauth2/access_token': 'http://open.mingdao.com/oauth2/auth2-access_token.html'
	'oauth2/verify_email': 'http://open.mingdao.com/oauth2/auth-verify_email.html'
	'search/fullsearch': 'http://open.mingdao.com/search/search-fullsearch.htm'

crawlApi = (item, callback) ->
	api = item.api
	url = urls[api]
	unless url then console.log api
	r.get url, (e, r, body) ->
		if e or not body then return callback e or new Error('request error')
		method_re = new RegExp '<h3>HTTP请求方式</h3>[\\s\\r\\n]*<p>(\\w+)</p>'
		method_m = body.match method_re
		item.method = method_m[1]
		table_re = new RegExp '<div class="open_con_table">([\\S\\s]*?)</div>', 'm'
		match = body.match(table_re)
		unless match
			console.log api
			return callback new Error('no match')
		table = match[1]
		tr_re = new RegExp '<tr.*?>([\\S\\s]*?)</tr>'
		td_re = new RegExp '<td.*?>([\\S\\s]*?)</td>'
		table = table.replace(tr_re, '')
		tr_m = table.match(tr_re)
		args = []
		while tr_m
			tr = tr_m[1]
			td_m = tr.match(td_re)
			arg = []
			while td_m
				td = td_m[1]
				arg.push td
				tr = tr.replace(td_re, '')
				td_m = tr.match(td_re)
			arg = {name: arg[0], required: arg[1] == 'true', type: arg[2], description: arg[3]}
			args.push arg
			table = table.replace(tr_re, '')
			tr_m = table.match(tr_re)
		item.args = args
		callback null, item

apis = []
count = 0
for k, v of o
	apis.push {api: k, description: v}
async.map apis, crawlApi, (err, results) ->
	fs.writeFileSync 'mingdao_api.json', JSON.stringify(results)