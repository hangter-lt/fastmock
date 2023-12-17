import React, { useState, useEffect, useId } from 'react';
import { Layout, Menu, theme, Card, Tag, Row, Col, Empty } from 'antd';
import { ClockCircleOutlined } from '@ant-design/icons';
import MenuItem from 'antd/es/menu/MenuItem';
import Item from 'antd/es/list/Item';
import axios from "axios";
import { API_REQUEST, API_REQUESTS, API_REQUESTS_CLOSE } from '../consts';



const { Content, Sider } = Layout;

type Item = {
  id?: number
  uri?: string
  method?: string
}
type Items = Item[]
const menuItems: Items = []
var menuItem: Items = []
const r: Reqres = {
  time: 0
}

type Reqres = {
  id?: number
  uri?: string
  method?: string
  header?: string
  params?: string
  code?: number
  content_type?: string
  content?: string
  result?: string
  reason?: string
  time: number
}


const Requests: React.FC = () => {
  const {
    token: { colorBgContainer },
  } = theme.useToken();


  const [reqs, setReqs] = useState(menuItems)
  const [rr, setRr] = useState(r)
  const linkId = useId()

  useEffect(() => {
    menuItem = []

    const eventSource = new EventSource(API_REQUESTS + linkId);
    eventSource.onopen = function () {
      console.log("open")
    }
    eventSource.onmessage = function (ev) {
      console.log("event")
      const item: Item = JSON.parse(ev.data);
      setReqs([item].concat(menuItem))
      menuItem.unshift(item)
    };
    eventSource.onerror = function () {
      console.log("error");
      eventSource.close();
    };

    return () => {
      axios.get(API_REQUESTS_CLOSE + linkId).then((res) => {
        console.log(res.data)
      })
      eventSource.close()
    }

  }, []);

  const getRequest = (id: number | undefined) => {
    axios.get(API_REQUEST + id).then((res) => {
      setRr(res.data)
    })
  }

  const reqTime = new Date(rr.time).toLocaleString()

  return (
    <Layout style={{ height: '100%', padding: '10px 0px', background: colorBgContainer }} >
      <Sider style={{ background: colorBgContainer, overflow: 'auto' }} width={300}>
        <Menu
          mode="inline"
          defaultSelectedKeys={[]}
          style={{ height: '100%' }}
          selectedKeys={[]}
        >
          {reqs.map((r) => (
            <MenuItem onClick={() => getRequest(r.id)} key={r.id} > <Tag color="#108ee9">{r.method}</Tag> {r.uri} </MenuItem>
          ))}
        </Menu>
      </Sider>
      {rr.id == undefined && (
        <Empty style={{ margin: 200 }} description={false} />
      )}
      {rr.id != undefined && (
        <Content style={{ padding: '30px 30px', display: "flex" }}>
          <Row style={{ width: "100%" }}>
            <Col span={8}>
              <Card title="请求" style={{ width: "100%" }}>
                <Card>
                  <Tag icon={<ClockCircleOutlined />} color="purple">
                    {reqTime}
                  </Tag>
                </Card>
                <Card>
                  <Tag color="#108ee9">{rr.method}</Tag>{rr.uri}
                </Card>
                <br />
                <Card title="header">
                  <p style={{ whiteSpace: "pre-wrap" }}>
                    {rr.header}
                  </p>
                </Card>
                <br></br>
                <Card title="params">
                  <p style={{ whiteSpace: "pre-wrap" }}>
                    {JSON.stringify(JSON.parse(rr.params == undefined || rr.params == '' ? '{}' : rr.params), null, 4)}
                  </p>
                </Card>
                <br></br>

              </Card>
            </Col>
            <Col span={14} offset={1}>
              <Card title="响应" style={{ width: "100%" }} >
                <Card>
                  <Tag color={rr.code == 200 ? '#87d068' : '#f50'}>{rr.code}</Tag>{rr.content_type}
                </Card>
                <br />
                <Card title="body">
                  <p style={{ whiteSpace: "pre-wrap" }}>
                    {rr.content}
                  </p>
                  {rr.reason}
                </Card>
              </Card>
            </Col>
          </Row>
        </Content>
      )}
    </Layout >
  );
};

export default Requests;