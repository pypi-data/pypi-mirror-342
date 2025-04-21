import os
import pytest
from unittest.mock import patch, MagicMock
from shangshanAI import snapshot_download
from shangshanAI.download import DownloadError

@pytest.fixture
def mock_responses():
    """创建模拟的API响应"""
    project_response = {
        "id": 123,
        "name": "text2img-tony"
    }
    
    tree_response = [
        {
            "type": "blob",
            "path": "model.bin",
            "mode": "100644"
        },
        {
            "type": "blob",
            "path": "config.json",
            "mode": "100644"
        },
        {
            "type": "blob",
            "path": ".git/config",  # 这个文件应该被跳过
            "mode": "100644"
        }
    ]
    
    return project_response, tree_response

def test_validate_model_id():
    """测试模型ID验证"""
    from shangshanAI.utils import validate_model_id
    
    # 有效的模型ID
    assert validate_model_id("tonysu/text2img-tony")
    assert validate_model_id("user-name/model-name")
    assert validate_model_id("user123/model_name")
    
    # 无效的模型ID
    assert not validate_model_id("invalid_model_id")
    assert not validate_model_id("user/name/model")
    assert not validate_model_id("/model-name")
    assert not validate_model_id("user/")

@patch('requests.get')
def test_snapshot_download_success(mock_get, mock_responses, tmp_path):
    """测试成功下载场景"""
    project_response, tree_response = mock_responses
    
    # 模拟API响应
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    
    def mock_get_side_effect(url, **kwargs):
        mock_response.json.return_value = (
            project_response if "projects/tonysu%2Ftext2img-tony" in url
            else tree_response if "repository/tree" in url
            else b"mock file content"
        )
        return mock_response
    
    mock_get.side_effect = mock_get_side_effect
    
    # 执行下载
    model_dir = snapshot_download(
        "tonysu/text2img-tony",
        cache_dir=str(tmp_path),
        token="test-token"
    )
    
    # 验证结果
    assert os.path.exists(model_dir)
    assert os.path.exists(os.path.join(model_dir, "model.bin"))
    assert os.path.exists(os.path.join(model_dir, "config.json"))
    assert not os.path.exists(os.path.join(model_dir, ".git/config"))

def test_snapshot_download_invalid_model_id():
    """测试无效模型ID"""
    with pytest.raises(ValueError, match="无效的模型ID格式"):
        snapshot_download("invalid_model_id")

@patch('requests.get')
def test_snapshot_download_network_error(mock_get):
    """测试网络错误场景"""
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    
    with pytest.raises(DownloadError, match="下载失败"):
        snapshot_download("tonysu/text2img-tony")

@patch('requests.get')
def test_snapshot_download_with_token(mock_get, mock_responses, tmp_path):
    """测试使用token的场景"""
    project_response, _ = mock_responses
    
    mock_response = MagicMock()
    mock_response.json.return_value = project_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    test_token = "test-token"
    snapshot_download("tonysu/text2img-tony", token=test_token)
    
    # 验证API调用中包含了token
    calls = mock_get.call_args_list
    assert any(
        call.kwargs.get('headers', {}).get('Authorization') == f"Bearer {test_token}"
        for call in calls
    )

def test_snapshot_download_custom_cache_dir(tmp_path):
    """测试自定义缓存目录"""
    custom_cache_dir = str(tmp_path / "custom_cache")
    
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        model_dir = snapshot_download(
            "tonysu/text2img-tony",
            cache_dir=custom_cache_dir
        )
        
        assert custom_cache_dir in model_dir
        assert os.path.exists(custom_cache_dir) 