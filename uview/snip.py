import immutables
from pxr import Usd, Ar
from pprint import pp
from pathlib import Path
from operator import itemgetter
fp = r"B:\read\cg\downloads\Kitchen_set\Kitchen_set\Kitchen_set_instanced.usd"
stage = Usd.Stage.Open(fp)
models = map(Usd.ModelAPI, stage.Traverse(predicate=Usd.PrimIsModel))
infos = {info for model in models if (info := immutables.Map(model.GetAssetInfo()))}

_resolveAr = Ar.GetResolver().Resolve
def resolved(assetPath):
    return _resolveAr(str(Path(str(assetPath.path))))

with Ar.ResolverContextBinder(stage.GetPathResolverContext()):
    pp(sorted((dict(i, resolvedPath=resolved(i['identifier'])) for i in infos), key=itemgetter('name')))
