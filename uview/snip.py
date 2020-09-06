from pxr import Usd, Ar
from pathlib import Path
from functools import lru_cache
from collections import defaultdict


def reportModelInfo(stage):
    _resolveAr = Ar.GetResolver().Resolve

    @lru_cache
    def resolve(identifier):
        return _resolveAr(str(Path(identifier)))

    missing_info = set()
    incomplete_info = defaultdict(set)
    unresolved_ids = defaultdict(set)

    with Ar.ResolverContextBinder(stage.GetPathResolverContext()):
        for prim in stage.Traverse(predicate=Usd.PrimIsModel):
            model = Usd.ModelAPI(prim)
            if not (model.IsKind("component") or model.IsKind("assembly")):
                continue  # only check for "important" kinds
            elif (info := model.GetAssetInfo()):
                if (missing := frozenset({"name", "identifier"} - set(info))):
                    incomplete_info[missing].add(prim)
                elif not resolve(info['identifier'].path):
                    unresolved_ids[info['identifier']].add(prim)
                continue
            missing_info.add(prim)

    return missing_info, incomplete_info, unresolved_ids


if __name__ == "__main__":
    from printree import ptree
    for filepath in {
        r"B:\read\cg\downloads\Kitchen_set\Kitchen_set\Kitchen_set.usd",
        r"B:\read\cg\downloads\Kitchen_set\Kitchen_set\Kitchen_set_instanced.usd",
        
        r"B:\read\cg\downloads\UsdSkelExamples\UsdSkelExamples\HumanFemale\HumanFemale.usd",
        r"B:\read\cg\downloads\UsdSkelExamples\UsdSkelExamples\HumanFemale\HumanFemale.walk.usd",
        r"B:\read\cg\downloads\UsdSkelExamples\UsdSkelExamples\HumanFemale\HumanFemale.keepAlive.usd",

        r"B:\read\cg\downloads\PointInstancedMedCity\PointInstancedMedCity.usd",
        r"B:\read\cg\downloads\Attic_NVIDIA_506\Attic_NVIDIA\Attic_NVIDIA.usd",
        r"B:\read\cg\downloads\esper_room_v3\esper_room_v3\EsperRoom.usda",
    }: 
        # continue
        print(f"\nChecking Model Asset Info on stage from {filepath=}")
        stage = Usd.Stage.Open(filepath)
        missing, incomplete, unresolved = reportModelInfo(stage)
        ptree(dict(missing=missing, incomplete=incomplete, unresolved=unresolved))
