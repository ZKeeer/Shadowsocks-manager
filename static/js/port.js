function restartServer() {
	//重启ss服务器
	$.ajax({
		"url": "/restartss",
		"type": "get",
		success: function() {},
		error: function() {
			alert("重启失败，请重试");
		}
	});
}

function loadPortInfo() {
	//加载port数据写入table
	//读取后台数据
	$.ajax({
		url: "/getportinfo",
		type: "get",
		dataType: "json",
		success: function(data) {
			writeIntoTable(data);
		},
		error: function(data) {
			alert("刷新失败，请重试");
		}
	});
}

function writeIntoTable(data) {
	//写入table
	//1.删除table数据
	var tb = document.getElementById('port_info_table');
	var rowNum = tb.rows.length;
	for(i = 1; i < rowNum; i++) {
		tb.deleteRow(i);
		rowNum = rowNum - 1;
		i = i - 1;
	}
	//2.重新写入
	var id = 0;
	for(var key in data) {
		//获取值
		id = id + 1;
		var table = $("#port_info_table");
		var row_id = "<td>" + id + "</td>";
		var port = "<td>" + data[key].port + "</td>";
		var passwd = "<td>" + data[key].passwd + "</td>";
		var used = "<td>" + data[key].used + "</td>";
		var limit = "<td>" + data[key].limit + "</td>";
		var speed = "<td>" + data[key].speed + "</td>";
		var settings = "<td><a id=\"" + id + "\" onclick=\"showModifyModal(this);modifyConfig(this);\" class=\"check_btn\">修改</a>&nbsp;&nbsp;<a id=\"" + id + "\" onclick=\"delThisRow(this)\" class=\"delete_btn\">删除</a></td>";
		var useable = "";
		if(data[key].useable == true) {
			useable = "<td>是</td>";
		} else {
			useable = "<td>否</td>";
		}
		table.append("<tr class=\"second-tr\">" + row_id + port + passwd + used + limit + speed + settings + useable + "</tr>");
	}
}

function delThisRow(obj) {
	//删除行
	var id = obj.parentNode.parentNode.rowIndex;
	var port = document.getElementById("port_info_table").rows[id].cells[1].innerText;
	document.getElementById("port_info_table").deleteRow(id);
	data = {
		"port": port
	}
	$.ajax({
		url: "/deloneport",
		type: "post",
		contentType: "application/json; charset=UTF-8",
		data: JSON.stringify(data)
	});
}

function showAddPortModal(obj) {
	//显示添加端口的modal
	$("#add_port").modal("show");
}

function addPortConfig(obj) {
	//给添加端口的模态传数据
	var table = document.getElementById("port_info_table");
	rows = table.rows.length;
	var maxid = 0;
	for(var i = 1; i < rows; i++) {
		if(maxid < parseInt(table.rows[i].cells[0].innerText)) {
			maxid = parseInt(table.rows[i].cells[0].innerText);
		}
	}
	var new_id = parseInt(maxid) + 1;
	$("#add_port_id").val(new_id);
}

function addPortConfirm(obj) {
	//获取模态数据
	var port = $("#add_port_port").val();
	var passwd = $("#add_port_passwd").val();
	var limit = $("#add_port_limit").val();
	var speed = $("#add_port_speed").val();
	var useable = $("#add_port_useable").val();
	//给后台的数据
	port_data = {
		"port": port,
		"passwd": passwd,
		"used": 0,
		"limit": limit,
		"speed": speed,
		"useable": useable,
		"type": "add"
	};
	//检查合法性
	//port合法性
	if(port != '') {
		var rex = /^\d{4,5}$/;
		if(rex.test(port)) {
			var table = document.getElementById("port_info_table");
			rows = table.rows.length;
			for(var i = 1; i < rows; i++) {
				if(port == table.rows[i].cells[1].innerText) {
					alert("端口重复");
					return;
				}
			}
		} else {
			alert("端口值不合法");
			return;
		}
	} else {
		alert("端口为空");
		return;
	}
	//limit合法性
	if(limit != '') {
		var rex = /^\d+$/;
		if(rex.test(limit) == false) {
			alert("流量上限不合法");
			return;
		}
	} else {
		alert("流量上限为空");
		return;
	}
	//speed合法性
	if(speed != '') {
		var rex = /^\d+$/;
		if(rex.test(speed) == false) {
			alert("限速值不合法");
			return;
		}
	} else {
		alert("限速值为空");
		return;
	}
	//useable合法性
	if(useable != '') {
		if(useable != '是' & useable != '否') {
			alert('端口可用性不合法');
			return;
		}
	} else {
		useable = "是";
	}
	//写回table
	var table = $("#port_info_table");
	var new_id = $("#add_port_id").val();
	id = "<td>" + $("#add_port_id").val() + "</td>";
	port = "<td>" + port + "</td>";
	passwd = "<td>" + passwd + "</td>";
	used = "<td>0</td>";
	limit = "<td>" + limit + "</td>";
	speed = "<td>" + speed + "</td>";
	var settings = "<td><a id=\"" + new_id + "\" onclick=\"showModifyModal(this);modifyConfig(this);\" class=\"check_btn\">修改</a>&nbsp;&nbsp;<a id=\"" + new_id + "\" onclick=\"delThisRow(this)\" class=\"delete_btn\">删除</a></td>";
	useable = "<td>" + useable + "</td>";
	table.append("<tr class=\"second-tr\">" + id + port + passwd + used + limit + speed + settings + useable + "</tr>");
	//关闭模态
	$("#add_port").modal("hide");
	//传给后台
	sendPortInfoToServer(port_data);
}

function sendPortInfoToServer(data) {
	//将端口数据传给后台
	$.ajax({
		url: "/postportinfo",
		type: "post",
		contentType: "application/json; charset=UTF-8",
		data: JSON.stringify(data)
	});
}

function modifyConfig(obj) {
	//给模态传数据
	//获取行id
	var row = obj.parentNode.parentNode.rowIndex;
	//获取行数据
	var id = document.getElementById("port_info_table").rows[row].cells[0].innerText;
	var port = document.getElementById("port_info_table").rows[row].cells[1].innerText;
	var passwd = document.getElementById("port_info_table").rows[row].cells[2].innerText;
	var used = document.getElementById("port_info_table").rows[row].cells[3].innerText;
	var limit = document.getElementById("port_info_table").rows[row].cells[4].innerText;
	var speed = document.getElementById("port_info_table").rows[row].cells[5].innerText;
	var btn_id = document.getElementById("port_info_table").rows[row].cells[6].innerText;
	var useable = document.getElementById("port_info_table").rows[row].cells[7].innerText;
	//给模态写入数据
	$("#modify_id").val(id);
	$("#modify_port").val(port);
	$("#modify_passwd").val(passwd);
	$("#modify_used").val(used);
	$("#modify_limit").val(limit);
	$("#modify_speed").val(speed);
	$("#modify_useable").val(useable);
	$("#rowid").val(row);
}

function showModifyModal(obj) {
	//显示修改端口的modal
	$("#modify_port_config").modal('show');
}

function updateConfig(element) {
	//从模态获取数据，写回table并传给后台。
	//获取模态数据
	var row = $("#rowid").val();
	var port = $("#modify_port").val();
	var passwd = $("#modify_passwd").val();
	var used = $("#modify_used").val();
	var limit = $("#modify_limit").val();
	var speed = $("#modify_speed").val();
	var useable = $("#modify_useable").val();
	//给后台的数据
	port_data = {
		"port": port,
		"passwd": passwd,
		"used": used,
		"limit": limit,
		"speed": speed,
		"useable": useable,
		"type": "modify"
	};
	//写回table
	document.getElementById("port_info_table").rows[row].cells[2].innerHTML = passwd;
	document.getElementById("port_info_table").rows[row].cells[3].innerHTML = used;
	document.getElementById("port_info_table").rows[row].cells[4].innerHTML = limit;
	document.getElementById("port_info_table").rows[row].cells[5].innerHTML = speed;
	document.getElementById("port_info_table").rows[row].cells[7].innerHTML = useable;
	//关闭模态
	$("#modify_port_config").modal('hide');
	//传给后台
	sendPortInfoToServer(port_data);
};
