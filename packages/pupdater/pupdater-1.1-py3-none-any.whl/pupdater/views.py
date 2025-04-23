import subprocess, json, csv
from django.contrib import messages
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, HttpResponse
from .models import PipFreezeSnapshot

@csrf_protect
def pip_manager_view(request):
    context = {
        "title": "🐾 Pupdater pip manager",
        "packages": [],
        "show_results": False,
        "show_snapshots": False,
        "snapshots": [],
        "snapshot_detail": None,
        "snapshot_packages": [],
        "compare_data": [],
        "compare_ids": [],
        "show_compare": False,
    }

    if request.method == "POST":

        if "run_freeze" in request.POST:

            try:
                output = subprocess.check_output(['pip', 'list', '--format=json'], text=True)
                installed = json.loads(output)

                outdated_output = subprocess.check_output(['pip', 'list', '--outdated', '--format=json'], text=True)
                outdated = {pkg['name'].lower(): pkg['latest_version'] for pkg in json.loads(outdated_output)}

                packages = []
                for pkg in installed:
                    name = pkg["name"]
                    try:
                        show_output = subprocess.check_output(['pip', 'show', name], text=True)
                        info = {
                            line.split(": ", 1)[0]: line.split(": ", 1)[1]
                            for line in show_output.strip().split("\n")
                            if ": " in line
                        }
                        packages.append({
                            "name": name,
                            "version": pkg["version"],
                            "outdated": outdated.get(name.lower()),
                            "summary": info.get("Summary", ""),
                            "homepage": info.get("Home-page", ""),
                            "author": info.get("Author", ""),
                            "license": info.get("License", ""),
                        })
                    except subprocess.CalledProcessError:
                        continue

                context["packages"] = packages
                context["show_results"] = True
                request.session["freeze_results"] = packages

            except Exception as e:
                messages.error(request, f"Freeze error: {e}")


        elif "upgrade_package" in request.POST:
            name = request.POST.get("upgrade_package")
            try:
                subprocess.check_output(['pip', 'install', '--upgrade', name], text=True)
            except Exception:
                pass  # geen melding

            packages = request.session.get("freeze_results", [])
            try:
                show_output = subprocess.check_output(['pip', 'show', name], text=True)
                info = {
                    line.split(": ", 1)[0]: line.split(": ", 1)[1]
                    for line in show_output.strip().split("\n")
                    if ": " in line
                }

                version_output = subprocess.check_output(['pip', 'list', '--format=json'], text=True)
                versions = json.loads(version_output)
                version = next((p["version"] for p in versions if p["name"].lower() == name.lower()), "–")

                outdated_output = subprocess.check_output(['pip', 'list', '--outdated', '--format=json'], text=True)
                outdated = {pkg['name'].lower(): pkg['latest_version'] for pkg in json.loads(outdated_output)}

                for pkg in packages:
                    if pkg["name"].lower() == name.lower():
                        pkg["version"] = version
                        pkg["outdated"] = outdated.get(name.lower())
                        pkg["summary"] = info.get("Summary", "")
                        pkg["homepage"] = info.get("Home-page", "")
                        pkg["author"] = info.get("Author", "")
                        pkg["license"] = info.get("License", "")

                context["packages"] = packages
                context["show_results"] = True
                request.session["freeze_results"] = packages

            except Exception:
                pass

        elif "save_snapshot" in request.POST:
            raw_data = request.session.get("freeze_results", [])
            if raw_data:
                PipFreezeSnapshot.objects.create(note=request.POST.get("note", ""), raw_data=raw_data)
                context["packages"] = raw_data
                context["show_results"] = True
            else:
                messages.warning(request, "⚠️ No freeze data to snapshot.")

        elif "view_snapshots" in request.POST or "back_to_list" in request.POST:
            context["show_snapshots"] = True
            context["snapshots"] = PipFreezeSnapshot.objects.order_by("-created")

        elif "view_snapshot_detail" in request.POST:
            sid = request.POST.get("view_snapshot_detail")
            try:
                snapshot = PipFreezeSnapshot.objects.get(pk=sid)
                context["snapshot_detail"] = snapshot
                context["snapshot_packages"] = snapshot.raw_data
            except PipFreezeSnapshot.DoesNotExist:
                messages.error(request, "Snapshot not found.")

        elif "delete_snapshot" in request.POST:
            sid = request.POST.get("delete_snapshot")
            try:
                PipFreezeSnapshot.objects.get(pk=sid).delete()
                context["show_snapshots"] = True
                context["snapshots"] = PipFreezeSnapshot.objects.order_by("-created")
            except PipFreezeSnapshot.DoesNotExist:
                messages.error(request, "Snapshot not found for deletion.")


#=======================

        elif "compare_snapshots" in request.POST:
            id1 = request.POST.get("snapshot_id_1")
            id2 = request.POST.get("snapshot_id_2")
            try:
                snap1 = PipFreezeSnapshot.objects.get(pk=id1)
                snap2 = PipFreezeSnapshot.objects.get(pk=id2)
                names = sorted(set(pkg["name"] for pkg in snap1.raw_data + snap2.raw_data))

                def lookup(data, name):
                    for pkg in data:
                        if pkg["name"] == name:
                            return pkg.get("version", "-")
                    return "❌"

                context["compare_data"] = [
                    {"name": name, "v1": lookup(snap1.raw_data, name), "v2": lookup(snap2.raw_data, name)}
                    for name in names
                ]

                request.session["compare_data"] = context["compare_data"]  # ✅ FIX HIER

                context["compare_ids"] = [snap1.created, snap2.created]
                context["compare_counts"] = [len(snap1.raw_data), len(snap2.raw_data)]
                context["show_compare"] = True
                context["show_snapshots"] = True
                context["snapshots"] = PipFreezeSnapshot.objects.order_by("-created")
            except Exception as e:
                messages.error(request, f"Compare error: {e}")






# =========================



        else:
            # fallback: toon bestaande freeze_results
            context["packages"] = request.session.get("freeze_results", [])
            if context["packages"]:
                context["show_results"] = True

    else:
        # Geen pip freeze info tonen bij lege GET-request
        context["packages"] = []
        context["show_results"] = False


    return TemplateResponse(request, "pupdater/pupdater_main.html", context)


@csrf_protect
def reqcheck_view(request):
    context = {
        "title": "🐾 Pupdater Requirements Check",
        "compare_data": [],
        "show_check": False,
    }

    if request.method == "POST" and ("add_to_requirements" in request.POST or "update_requirement" in request.POST):
        name = request.POST.get("package")
        version = request.POST.get("version")
        regel = f"{name}=={version}"
        try:
            try:
                with open("requirements.txt", "r") as f:
                    regels = [r.strip() for r in f.readlines()]
            except FileNotFoundError:
                regels = []

            regels_dict = {r.split("==")[0].lower(): r for r in regels if "==" in r}
            regels_dict[name.lower()] = regel

            with open("requirements.txt", "w") as f:
                for r in sorted(regels_dict.values()):
                    f.write(r + "\n")

        except Exception as e:
            messages.error(request, f"⚠️ Schrijven mislukt: {e}")

    if request.method == "POST" and ("run_reqcheck" in request.POST or "add_to_requirements" in request.POST or "update_requirement" in request.POST):
        try:
            output = subprocess.check_output(['pip', 'freeze'], text=True)
            installed_lines = output.strip().split("\n")
            installed = {
                line.split("==")[0].lower(): line.split("==")[1]
                for line in installed_lines if "==" in line
            }

            try:
                with open("requirements.txt") as f:
                    req_lines = [line.strip() for line in f if "==" in line]
                    required = {
                        line.split("==")[0].lower(): line.split("==")[1]
                        for line in req_lines
                    }
            except FileNotFoundError:
                required = {}

            compare_data = []
            for name, version in installed.items():
                req_version = required.get(name)
                if req_version is None:
                    status = "➕ Unlisted"
                elif req_version != version:
                    status = "🔄 Update"
                else:
                    status = "✅ Listed"
                compare_data.append({
                    "name": name,
                    "installed": version,
                    "required": req_version or "–",
                    "status": status,
                })

            context["compare_data"] = compare_data
            request.session["compare_data"] = compare_data
            context["show_check"] = True

        except Exception as e:
            messages.error(request, f"❌ Fout tijdens vergelijking: {e}")

    return TemplateResponse(request, "pupdater/requirements_check.html", context)


def export_json(request, mode, snapshot_id=None):
    try:
        if mode == "snapshot":
            snapshot = PipFreezeSnapshot.objects.get(pk=snapshot_id)
            data = snapshot.raw_data
            filename = f"snapshot_{snapshot_id}.json"
        elif mode == "requirements":
            data = request.session.get("compare_data", [])
            filename = "requirements_check.json"
        elif mode == "freeze":
            data = request.session.get("freeze_results", [])
            filename = "pip_freeze.json"
        elif mode == "compare":
            data = request.session.get("compare_data", [])
            filename = "snapshot_compare.json"
        else:
            raise ValueError("Invalid mode")

        if not data:
            raise ValueError("No data found")

        content = json.dumps(data, indent=2)
        response = HttpResponse(content, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception:
        return HttpResponse("Data not found", status=404)


def export_csv(request, mode, snapshot_id=None):
    try:
        if mode == "snapshot":
            snapshot = PipFreezeSnapshot.objects.get(pk=snapshot_id)
            data = snapshot.raw_data
            filename = f"snapshot_{snapshot_id}.csv"
        elif mode == "requirements":
            data = request.session.get("compare_data", [])
            filename = "requirements_check.csv"
        elif mode == "freeze":
            data = request.session.get("freeze_results", [])
            filename = "pip_freeze.csv"
        elif mode == "compare":
            data = request.session.get("compare_data", [])
            filename = "snapshot_compare.csv"
        else:
            raise ValueError("Invalid mode")

        if not data:
            raise ValueError("No data found")

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.DictWriter(response, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return response
    except Exception:
        return HttpResponse("Data not found", status=404)


def export_txt(request, mode, snapshot_id=None):
    try:
        if mode == "snapshot":
            snapshot = PipFreezeSnapshot.objects.get(pk=snapshot_id)
            data = snapshot.raw_data
            filename = f"snapshot_{snapshot_id}.txt"
        elif mode == "requirements":
            data = request.session.get("compare_data", [])
            filename = "requirements_check.txt"
        elif mode == "freeze":
            data = request.session.get("freeze_results", [])
            filename = "pip_freeze.txt"
        elif mode == "compare":
            data = request.session.get("compare_data", [])
            filename = "snapshot_compare.txt"
        else:
            raise ValueError("Invalid mode")

        if not data:
            raise ValueError("No data found")

        content = json.dumps(data, indent=2)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception:
        return HttpResponse("Data not found", status=404)

