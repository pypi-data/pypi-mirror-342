import os
import shutil
import click
import importlib.resources

@click.command()
@click.argument('project_name')
@click.option('--path', '-p', default='.', help='프로젝트를 생성할 경로')
def main(project_name, path):
    """프로젝트를 생성하는 CLI 도구입니다."""
    try:
        # 프로젝트 경로 생성
        project_path = os.path.join(path, project_name)
        os.makedirs(project_path, exist_ok=True)
        
        # .cursor 디렉토리 생성
        cursor_dir = os.path.join(project_path, '.cursor')
        os.makedirs(cursor_dir, exist_ok=True)
        
        # 패키지의 .cursor 디렉토리 경로 가져오기
        with importlib.resources.path('cursor_boilerplate', '.cursor') as current_cursor_dir:
            # 현재 디렉토리의 .cursor 파일들을 복사
            for item in os.listdir(current_cursor_dir):
                src = os.path.join(current_cursor_dir, item)
                dst = os.path.join(cursor_dir, item)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                elif os.path.isdir(src):
                    shutil.copytree(src, dst)
        
        click.echo(f"프로젝트 '{project_name}'이 성공적으로 생성되었습니다.")
        click.echo(f"경로: {os.path.abspath(project_path)}")
        
    except Exception as e:
        click.echo(f"오류가 발생했습니다: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main() 