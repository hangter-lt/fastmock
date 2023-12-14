import { Link, Outlet } from "react-router-dom";
import { Layout, Menu, MenuProps } from 'antd';
const { Header, Content } = Layout;
import logo from "./static/logo.png"


const items: MenuProps['items'] = [
    {
        label: (
            <Link to="/mock/requests">实时请求</Link>
        ),
        key: 'requests',
    },
    {
        label: (
            <Link to="/mock/files">MOCK文件</Link>
        ),
        key: 'files',
    }
];

const Frame: React.FC = () => {
    return (
        <Layout style={{ height: '100%' }}>
            <Header style={{ display: 'flex', alignItems: 'center', backgroundColor: "white", borderBottomColor:"#F0F0F0", borderBottomStyle: "solid", borderBottomWidth: "thin"}}>
                <div style={{ width: "200px", display: "flex", justifyContent: "space-evenly" }}>
                    <Link to="/" style={{ display: "flex", justifyContent: "space-evenly" }}>
                        <img src={logo} width={180} />
                    </Link>
                </div>
                <Menu mode="horizontal" items={items} />
            </Header>
            <Content style={{ padding: '0 50px', height: '100%' }}>
                <Outlet />
            </Content>
        </Layout>
    );
}

export default Frame