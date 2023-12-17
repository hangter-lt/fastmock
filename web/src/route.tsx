import { MemoryRouter, Navigate, Route, Routes } from "react-router-dom"
import Requests from "./api/requests";
import ApiFiles from "./api/apifiles";
import Frame from "./frame";
import { Empty } from 'antd';

function Router() {
    return (
        <MemoryRouter>
            <Routes>
                <Route path="/" element={ <Navigate replace to="/mock/home" />} />
                <Route path="/mock"  element={<Frame />} >
                    <Route path="home" element={<Home />} />
                    <Route path="requests" element={<Requests />} />
                    <Route path="files" element={<ApiFiles />} />
                </Route>
            </Routes>
        </MemoryRouter>
    )
}

const Home = () => <Empty style={{margin: 200}} description={false} />;

export default Router;

