import json
import os
from typing import Any, Dict, List, Tuple
from python_on_whales import docker, Image, DockerException
from python_on_whales.utils import run
from python_on_whales.docker_client import DockerClient
from .config.build_config import ImageBuildConfig


def get_client():
    if os.environ.get("HMD_DOCKER_USE_NERDCTL", "false") == "false":
        print("USING DOCKER")
        return docker
    print("USING NERDCTL")
    return DockerClient(client_call=["hmd_nerdctl"])


def build_image_dest(tag: str):
    return f"./{tag.replace('/', '_').replace(':', '_')}.tar"


def build_platform_tag(tag: str, version: str, platform: str):
    return f"{tag}:{version}-{platform.replace('/', '-')}"


def build_image(tag: str, version: str, config: ImageBuildConfig) -> List[Image]:
    docker = get_client()
    images: List[Image] = []
    build_args = {**config.build_args}
    if os.environ.get("HMD_DOCKER_USE_NERDCTL", "false") == "false":
        buildx_builder = docker.buildx.create(
            use=True,
            driver="docker-container",
            driver_options={"network": "host"},
            buildkitd_flags="--allow-insecure-entitlement network.host",  # Allows for network host option for building in Argo
        )

        with buildx_builder:
            for platform in config.platforms:
                print(f"Building image {tag}:{version} for platform {platform}")
                image = docker.build(
                    config.context_dir,
                    build_args={**build_args, "PLATFORM": platform.split("/")[-1]},
                    tags=build_platform_tag(tag, version, platform),
                    cache=config.cache,
                    file=config.dockerfile,
                    secrets=[
                        (
                            f"id={secret.id},src={secret.src}"
                            if secret.src is not None
                            else f"id={secret.id}"
                        )
                        for secret in config.secrets
                    ],
                    platforms=[platform],
                    progress=config.progress,
                    network=config.network,
                    output={
                        "type": "docker",
                        "name": build_platform_tag(tag, version, platform),
                    },
                )

                images.append(image)
        if len(images) == 1:
            if isinstance(images[0], str):
                docker.tag(images[0], f"{tag}:{version}")
            else:
                images[0].tag(f"{tag}:{version}")
    else:
        print(f"Building image {tag}:{version} for platform {config.platforms}")
        lines = docker.build(
            config.context_dir,
            build_args=config.build_args,
            tags=f"{tag}:{version}",
            cache=config.cache,
            file=config.dockerfile,
            secrets=[
                (
                    f"id={secret.id},src={secret.src}"
                    if secret.src is not None
                    else f"id={secret.id}"
                )
                for secret in config.secrets
            ],
            platforms=config.platforms,
            progress=config.progress,
            stream_logs=True,
        )
        for ln in lines:
            print(ln)

        for platform in config.platforms:
            lines = docker.build(
                config.context_dir,
                build_args={**build_args, "PLATFORM": platform.split("/")[-1]},
                tags=build_platform_tag(tag, version, platform),
                cache=True,
                file=config.dockerfile,
                secrets=[
                    (
                        f"id={secret.id},src={secret.src}"
                        if secret.src is not None
                        else f"id={secret.id}"
                    )
                    for secret in config.secrets
                ],
                platforms=[platform],
                progress=config.progress,
                stream_logs=True,
            )
            for ln in lines:
                print(ln)

        images.append(f"{tag}:{version}")

    return images


def publish_image(tag: str, version: str, config: ImageBuildConfig):
    images = []
    latest_images = []
    docker = get_client()

    if os.environ.get("HMD_DOCKER_USE_NERDCTL", "false") == "false":
        for platform in config.platforms:
            img_tag = build_platform_tag(tag, version, platform)
            docker.push(img_tag)
            images.append(img_tag)

            latest_tag = build_platform_tag(tag, "latest", platform)
            docker.tag(img_tag, latest_tag)
            docker.push(latest_tag)
            latest_images.append(latest_tag)
        docker.manifest.create(name=f"{tag}:{version}", manifests=images)

        docker.manifest.push(f"{tag}:{version}", purge=True)

        docker.manifest.create(name=f"{tag}:latest", manifests=latest_images)

        docker.manifest.push(f"{tag}:latest", purge=True)
    else:
        img_tag = f"{tag}:{version}"
        # docker.push(f"{tag}:{version}")
        cmd = docker.docker_cmd + ["push", "--all-platforms", img_tag]
        run(cmd)

        docker.tag(img_tag, f"{tag}:latest")
        cmd = docker.docker_cmd + ["push", "--all-platforms", f"{tag}:latest"]
        run(cmd)

        for platform in config.platforms:
            platform_tag = build_platform_tag(tag, version, platform)
            cmd = docker.docker_cmd + ["push", f"--platform={platform}", platform_tag]
            run(cmd)
            latest_tag = build_platform_tag(tag, "latest", platform)
            docker.tag(platform_tag, latest_tag)
            cmd = docker.docker_cmd + ["push", f"--platform={platform}", latest_tag]
            run(cmd)


def pull_images(
    tag: str, version, config: ImageBuildConfig, platforms: List[str] = None
) -> Dict[str, str]:
    images = {}

    docker = get_client()
    if platforms is None:
        platforms = config.platforms

    for platform in platforms:
        try:
            img_tag = build_platform_tag(tag, version, platform)
            img = docker.pull(img_tag)
            images[platform] = img_tag
            continue
        except DockerException as e:
            pass

        try:
            img_tag = build_platform_tag(tag, version, platform)
            print(
                docker.docker_cmd
                + ["pull", f"--platform={platform}", f"{tag}:{version}"]
            )
            ret = run(
                docker.docker_cmd
                + ["pull", f"--platform={platform}", f"{tag}:{version}"]
            )
            print(ret)
            docker.tag(f"{tag}:{version}", img_tag)
            images[platform] = img_tag
        except DockerException as e:
            print(
                f'Failed running: {docker.docker_cmd + ["pull", "--platform", platform, f"{tag}:{version}"]}'
            )
            pass

    if len(images) == 0:
        img_tag = f"{tag}:{version}"
        docker.pull(f"{tag}:{version}")
        images["none"] = img_tag

    print(images)
    return images


def deploy_images(
    image_dict: Dict[str, str],
    target_tag: str,
    version: str,
    config: ImageBuildConfig,
    target_platform: str = None,
):
    docker = get_client()
    images = []

    if "none" in image_dict:
        img = image_dict.get("none")

        if img is not None:
            new_tag = f"{target_tag}:{version}"
            docker.tag(img, new_tag)
            docker.push(new_tag)

            return
    if target_platform is not None:
        img = image_dict.get(target_platform)
        print(img)
        if img is None:
            raise Exception(
                f"Cannot find image for {target_tag}:{version} on target platform {target_platform}"
            )

        new_tag = f"{target_tag}:{version}"
        print(new_tag)
        docker.tag(img, new_tag)
        docker.push(new_tag)
    else:
        for platform in config.platforms:
            img = image_dict.get(platform)

            if img is not None:
                new_tag = build_platform_tag(target_tag, version, platform)
                docker.tag(img, new_tag)
                docker.push(new_tag)
                images.append(new_tag)

        docker.manifest.create(name=f"{target_tag}:{version}", manifests=images)
        print("PUSHING MANIFEST", images)
        docker.manifest.push(f"{target_tag}:{version}", purge=True)


def run_container(
    image: str,
    name: str = None,
    entrypoint: str = None,
    command: List[str] = None,
    network: str = None,
    environment: Dict[str, Any] = {},
    volumes: List[Tuple[str, str]] = [],
    detach: bool = False,
):
    client = get_client()
    envs = {}

    for k, v in environment.items():
        if isinstance(v, dict):
            envs[k] = json.dumps(v)
        elif isinstance(v, list):
            envs[k] = json.dumps(v)
        else:
            envs[k] = v

    run_args = {"image": image, "envs": envs, "volumes": volumes, "detach": detach}

    if name is not None:
        run_args["name"] = name

    if entrypoint is not None:
        run_args["entrypoint"] = entrypoint

    if command is not None:
        run_args["command"] = command

    if network is not None:
        run_args["networks"] = [network]

    return client.run(**run_args)


def kill_container(container):
    client = get_client()

    client.kill(container)
